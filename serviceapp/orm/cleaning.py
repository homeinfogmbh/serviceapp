"""Cleaning entries."""

from datetime import datetime

from peewee import DateTimeField
from peewee import ForeignKeyField

from peeweeplus import EnumField

from serviceapp.enumerations import CleaningType
from serviceapp.orm.common import BaseModel
from serviceapp.orm.user import User


__all__ = ['Cleaning']


class Cleaning(BaseModel):
    """A cleaning record."""

    user = ForeignKeyField(
        User, column_name='user', lazy_load=False, on_delete='CASCADE'
    )
    type = EnumField(CleaningType)
    start = DateTimeField(default=datetime.now)
    end = DateTimeField(null=True)
