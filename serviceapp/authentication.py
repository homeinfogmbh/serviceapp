"""Authentication decorators."""

from functools import wraps
from typing import Any, Callable

from wsgilib import JSONMessage

from serviceapp.localproxies import get_current_user


__all__ = ["authenticated"]


def authenticated(function: Callable) -> Callable:
    """Decorates the given function with authentication."""

    @wraps(function)
    def wrapper(*args, **kwargs) -> Any:
        if get_current_user().can_login:
            raise JSONMessage("Account locked.")

        return function(*args, **kwargs)

    return wrapper
