"""Object-relational mappings."""

from datetime import datetime

from peewee import BooleanField, DateTimeField, ForeignKeyField

from peeweeplus import Argon2Field
from peeweeplus import EnumField
from peeweeplus import JSONModel
from peeweeplus import MySQLDatabaseProxy

from serviceapp.enumerations import CleaningType
from serviceapp.pwgen import genpw


__all__ = ['DATABASE', 'User', 'Session', 'Cleaning']


DATABASE = MySQLDatabaseProxy('serviceapp')


class BaseModel(JSONModel):
    """Base model for this database."""

    class Meta:
        database = DATABASE
        schema = database.DATABASE


class User(BaseModel):
    """A service app user account."""

    password = Argon2Field()
    locked = BooleanField(default=False)


class Session(BaseModel):
    """Session information."""

    user = ForeignKeyField(
        User, column_name='user', lazy_load=False, on_delete='CASCADE'
    )
    secret = Argon2Field()

    @classmethod
    def open(cls, user: User) -> tuple[int, str]:
        """Opens a session for the given user."""
        session = cls(user=user, secret=(secret := genpw(32)))
        session.save()
        return session.id, secret


class Cleaning(BaseModel):
    """A cleaning record."""

    user = ForeignKeyField(
        User, column_name='user', lazy_load=False, on_delete='CASCADE'
    )
    type = EnumField(CleaningType)
    start = DateTimeField(default=datetime.now)
    end = DateTimeField(null=True)
