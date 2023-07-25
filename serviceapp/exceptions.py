"""Common exceptions."""


__all__ = ["InvalidPassword", "NonceUsed", "UserLocked"]


class InvalidPassword(Exception):
    """Indicates that an invalid password was provided."""


class NonceUsed(Exception):
    """Indicates that a nonce has already been used."""


class UserLocked(Exception):
    """Indicates that the user is locked."""
