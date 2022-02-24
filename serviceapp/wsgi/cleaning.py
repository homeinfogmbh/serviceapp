"""Add cleanings."""

from wsgilib import JSONMessage


__all__ = ['ROUTES']


def start_cleaning() -> JSONMessage:
    """Starts a new cleaning entry."""

    pass


ROUTES = [
    ('POST', '/cleaning', 'start_cleaning')
]
