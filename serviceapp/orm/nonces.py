"""Numbers used once."""

from __future__ import annotations
from typing import Union
from uuid import UUID, uuid4

from peewee import ForeignKeyField, Select, UUIDField

from mdb import Company, Customer

from serviceapp.exceptions import NonceUsed
from serviceapp.orm.common import BaseModel
from serviceapp.orm.user import User


__all__ = ["AuthorizationNonce"]


class AuthorizationNonce(BaseModel):
    """Nonce to authorize clients for users."""

    class Meta:
        table_name = "authorization_nonce"

    user = ForeignKeyField(
        User, column_name="user", on_delete="CASCADE", lazy_load=False
    )
    uuid = UUIDField(default=uuid4)

    @classmethod
    def add(cls, user: Union[User, int]) -> AuthorizationNonce:
        """Returns a new nonce for the given user."""
        nonce = cls(user=user)
        nonce.save()
        return nonce

    @classmethod
    def select(cls, *args, cascade: bool = False) -> Select:
        """Selects records."""
        if not cascade:
            return super().select(*args)

        return (
            super()
            .select(*{cls, User, Customer, Company, *args})
            .join(User)
            .join(Customer)
            .join(Company)
        )

    @classmethod
    def use(cls, uuid: UUID) -> AuthorizationNonce:
        """Uses a nonce and returns its user."""
        try:
            nonce = cls.select(cascade=True).where(cls.uuid == uuid).get()
        except cls.DoesNotExist:
            raise NonceUsed() from None

        nonce.delete_instance()
        return nonce
