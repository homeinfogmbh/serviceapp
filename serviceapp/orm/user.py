"""Users."""

from argon2.exceptions import VerifyMismatchError

from peewee import BooleanField
from peewee import ForeignKeyField
from peewee import Select
from peewee import SmallIntegerField

from mdb import Customer
from peeweeplus import Argon2Field

from serviceapp.constants import MAX_FAILED_LOGINS
from serviceapp.exceptions import InvalidPassword, UserLocked
from serviceapp.orm.common import BaseModel


__all__ = ['User']


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
