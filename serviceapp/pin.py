"""PIN handling."""

from string import digits, ascii_letters
from typing import NamedTuple

from basex import decode, encode


__all__ = ['decode_pin', 'encode_pin']


class Credentials(NamedTuple):
    """User login credentials."""

    id: int
    passwd: str


def b62encode(number: int) -> str:
    """Base62 encodes a non-negative integer."""

    return ''.join(reversed(encode(number, pool=digits+ascii_letters)))


def b62decode(code: str) -> int:
    """Base62-decodes a non-negative integer."""

    return decode(''.join(reversed(code)), pool=digits+ascii_letters)


def decode_pin(pin: str, *, id_size: int = 2) -> Credentials:
    """Returns the user ID and password from the PIN."""

    if len(pin) <= id_size:
        raise ValueError('PIN too short.')

    return Credentials(b62decode(pin[:id_size]), pin[id_size:])


def encode_pin(uid: int, passwd: str, *, id_size: int = 2) -> str:
    """Encodes a user ID and a password into a PIN."""

    if len(uid := b62encode(uid).ljust(id_size, '0')) != id_size:
        raise ValueError('Cannot b62encode UID:', uid)

    return uid + passwd
