"""Add cleanings."""

from flask import request

from wsgilib import JSONMessage

from serviceapp.localproxies import USER
from serviceapp.oauth2 import REQUIRE_OAUTH
from serviceapp.orm import Cleaning


__all__ = ['ROUTES']


@REQUIRE_OAUTH('cleaning')
def submit_cleaning() -> JSONMessage:
    """Starts a new cleaning entry."""

    cleaning = Cleaning.from_json(request.json, USER.id)
    cleaning.save()
    return JSONMessage('Cleaning submitted.', id=cleaning.id, status=201)


ROUTES = [
    ('POST', '/cleaning', submit_cleaning)
]
