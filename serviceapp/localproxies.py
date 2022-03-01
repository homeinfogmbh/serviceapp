"""Local proxies."""

from authlib.integrations.flask_oauth2 import current_token
from werkzeug.local import LocalProxy

from serviceapp.exceptions import UserLocked
from serviceapp.orm import User


__all__ = ['USER', 'CUSTOMER']


def get_user() -> User:
    """Performs authentication checks."""

    if (user := User.select(cascade=True).where(
            User.id == current_token.user
    ).get()).locked:
        raise UserLocked()

    return user


USER = LocalProxy(get_user)
CUSTOMER = LocalProxy(lambda: USER.customer)
