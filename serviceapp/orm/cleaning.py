"""Cleaning entries."""

from __future__ import annotations
from datetime import datetime
from typing import Union

from peewee import BooleanField, DateTimeField, ForeignKeyField

from serviceapp.orm.common import BaseModel
from serviceapp.orm.user import User


__all__ = ["Cleaning"]


class Cleaning(BaseModel):
    """A cleaning record."""

    user = ForeignKeyField(
        User, column_name="user", lazy_load=False, on_delete="CASCADE"
    )
    start = DateTimeField(default=datetime.now)
    end = DateTimeField(null=True)
    staircase = BooleanField(default=False)
    attic = BooleanField(default=False)
    basement = BooleanField(default=False)
    windows = BooleanField(default=False)

    @classmethod
    def from_json(cls, json: dict, user: Union[User, int], **kwargs) -> Cleaning:
        """Creates a cleaning record from a JSON-ish dict."""
        record = super().from_json(json, **kwargs)
        record.user = user
        return record
