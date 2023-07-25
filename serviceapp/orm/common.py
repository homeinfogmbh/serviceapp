"""Common ORM models."""

from peeweeplus import JSONModel
from peeweeplus import MySQLDatabaseProxy


__all__ = ["DATABASE", "BaseModel"]


DATABASE = MySQLDatabaseProxy("serviceapp")


class BaseModel(JSONModel):
    """Base model for this database."""

    class Meta:
        database = DATABASE
        schema = database.DATABASE
