"""Local proxies."""

from argon2.exceptions import VerifyMismatchError
from flask import request
from werkzeug.local import LocalProxy

from wsgilib import JSONMessage

from serviceapp.orm import User, Session
from serviceapp.pin import decode_pin


__all__ = ['SESSION', 'USER', 'login_user']


INVALID_PIN = JSONMessage('Invalid PIN.')
INVALID_SESSION = JSONMessage('Invalid session.')


def get_session() -> Session:
    """Returns the current session."""

    if (ident := request.headers.get('session-id')) is None:
        raise JSONMessage('No session ID specified.')

    if (secret := request.headers.get('session-secret')) is None:
        raise JSONMessage('No session secret specified.')

    try:
        ident = int(ident)
    except ValueError:
        raise INVALID_SESSION from None

    try:
        session = Session.select(Session, User).join(User).where(
            Session.id == ident
        ).get()
    except Session.DoesNotExist:
        raise INVALID_SESSION from None

    try:
        session.secret.verify(secret)
    except VerifyMismatchError:
        raise INVALID_SESSION from None

    return session


def login_user() -> User:
    """Returns the current user."""

    if (pin := request.headers.get('pin')) is None:
        raise JSONMessage('No PIN provided.')

    try:
        ident, passwd = decode_pin(pin)
    except ValueError:
        raise INVALID_PIN from None

    try:
        user = User[ident]
    except User.DoesNotExist:
        raise INVALID_PIN from None

    try:
        user.password.verify(passwd)
    except VerifyMismatchError:
        raise INVALID_PIN from None

    return user


SESSION = LocalProxy(get_session)
USER = LocalProxy(lambda: SESSION.user)
