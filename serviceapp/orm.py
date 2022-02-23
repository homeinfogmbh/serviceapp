"""Object-relational mappings."""

from datetime import datetime

from peewee import DateTimeField, ForeignKeyField

from peeweeplus import EnumField, JSONModel, MySQLDatabaseProxy

from serviceapp.enumerations import CleaningType


__all__ = ['DATABASE', 'User', 'Cleaning']


DATABASE = MySQLDatabaseProxy('serviceapp')


class BaseModel(JSONModel):
    """Base model for this database."""

    class Meta:
        database = DATABASE
        schema = database.DATABASE


class User(BaseModel):
    """Base model for a user."""


class Cleaning(BaseModel):
    """A cleaning record."""

    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')
    type = EnumField(CleaningType)
    start = DateTimeField(default=datetime.now)
    end = DateTimeField(null=True)
