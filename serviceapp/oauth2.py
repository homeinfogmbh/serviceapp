"""OAuth 2 framework."""

from oauth2gen import create_framework

from serviceapp.config import get_oauth2
from serviceapp.orm import User


__all__ = ['FRAMEWORK', 'REQUIRE_OAUTH', 'Token', 'create_tables']


FRAMEWORK = create_framework(User, get_oauth2())
REQUIRE_OAUTH = FRAMEWORK.resource_protector
Token = FRAMEWORK.models.token


def create_tables():
    """Creates the tables for the ComCat database."""

    for model in FRAMEWORK.models:
        model.create_table()
