"""Local proxies."""

from flask import request
from werkzeug.local import LocalProxy

from wsgilib import JSONMessage

from serviceapp.orm import User
from serviceapp.pin import decode_pin


__all__ = ['USER', 'get_current_user']


INVALID_PIN = JSONMessage('Invalid PIN.')


def get_current_user() -> User:
    """Returns the current user."""

    if (pin := request.headers.get('pin')) is None:
        raise JSONMessage('No PIN provided.')

    try:
        ident, passwd = decode_pin(pin)
    except ValueError:
        raise INVALID_PIN

    try:
        user = User[ident]
    except User.DoesNotExist:
        raise INVALID_PIN

    if user.password.verify(passwd):
        return user

    raise INVALID_PIN


USER = LocalProxy(get_current_user)
