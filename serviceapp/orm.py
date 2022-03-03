"""Object-relational mappings."""

from __future__ import annotations
from argon2.exceptions import VerifyMismatchError
from datetime import datetime
from typing import Union
from uuid import UUID, uuid4

from peewee import BooleanField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import Select
from peewee import SmallIntegerField
from peewee import UUIDField

from mdb import Company, Customer
from peeweeplus import Argon2Field
from peeweeplus import EnumField
from peeweeplus import JSONModel
from peeweeplus import MySQLDatabaseProxy

from serviceapp.constants import MAX_FAILED_LOGINS
from serviceapp.enumerations import CleaningType
from serviceapp.exceptions import InvalidPassword, NonceUsed, UserLocked


__all__ = ['DATABASE', 'User', 'AuthorizationNonce', 'Cleaning']


DATABASE = MySQLDatabaseProxy('serviceapp')


class BaseModel(JSONModel):
    """Base model for this database."""

    class Meta:
        database = DATABASE
        schema = database.DATABASE


class User(BaseModel):
    """A service app user account."""

    customer = ForeignKeyField(
        Customer, table_name='customer', lazy_load=False, on_delete='CASCADE'
    )
    passwd = Argon2Field()
    locked = BooleanField(default=False)
    failed_logins = SmallIntegerField(default=0)

    @classmethod
    def select(cls, *args, cascade: bool = False) -> Select:
        """Selects records."""
        if not cascade:
            return super().select(*args)

        return cls.select(*{cls, Customer, *args}).join(Customer)

    @property
    def can_login(self) -> bool:
        """Determines whether the user can log in."""
        return not self.locked and self.failed_logins < MAX_FAILED_LOGINS

    def login(self, passwd: str) -> bool:
        """Authenticates the user."""
        if not self.can_login:
            raise UserLocked()

        try:
            self.passwd.verify(passwd)
        except VerifyMismatchError:
            self.failed_logins += 1
            self.save()
            raise InvalidPassword() from None

        if self.passwd.needs_rehash:
            self.passwd = passwd
            self.save()

        return True


class AuthorizationNonce(BaseModel):
    """Nonce to authorize clients for users."""

    class Meta:
        table_name = 'authorization_nonce'

    user = ForeignKeyField(
        User, column_name='user', on_delete='CASCADE', lazy_load=False
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

        return super().select(*{
            cls, User, Customer, Company, *args
        }).join(User).join(Customer).join(Company)

    @classmethod
    def use(cls, uuid: UUID) -> AuthorizationNonce:
        """Uses a nonce and returns its user."""
        try:
            nonce = cls.select(cascade=True).where(cls.uuid == uuid).get()
        except cls.DoesNotExist:
            raise NonceUsed() from None

        nonce.delete_instance()
        return nonce


class Cleaning(BaseModel):
    """A cleaning record."""

    user = ForeignKeyField(
        User, column_name='user', lazy_load=False, on_delete='CASCADE'
    )
    type = EnumField(CleaningType)
    start = DateTimeField(default=datetime.now)
    end = DateTimeField(null=True)
