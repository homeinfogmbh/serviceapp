"""Object-relational mappings."""

from datetime import datetime

from peewee import BooleanField, DateTimeField, ForeignKeyField

from peeweeplus import Argon2Field
from peeweeplus import EnumField
from peeweeplus import JSONModel
from peeweeplus import MySQLDatabaseProxy

from serviceapp.enumerations import CleaningType


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


class Cleaning(BaseModel):
    """A cleaning record."""

    user = ForeignKeyField(
        User, column_name='user', lazy_load=False, on_delete='CASCADE'
    )
    type = EnumField(CleaningType)
    start = DateTimeField(default=datetime.now)
    end = DateTimeField(null=True)
