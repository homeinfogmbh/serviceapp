"""User login."""

from argon2.exceptions import VerifyMismatchError
from flask import request
from wsgilib import JSONMessage

from serviceapp.orm import User
from serviceapp.pin import decode_pin


__all__ = ['ROUTES']


INVALID_PIN = JSONMessage('Invalid PIN.')


def login() -> JSONMessage:
    """Logs in the user."""

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

    ident, secret = Session.open(user)

