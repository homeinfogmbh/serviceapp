"""PIN handling."""

from functools import partial
from string import digits, ascii_letters

from basex import decode, encode


__all__ = ['decode_pin', 'encode_pin']


b62encode = partial(encode, pool=digits+ascii_letters)
b62decode = partial(decode, pool=digits+ascii_letters)


def decode_pin(pin: str) -> tuple[int, str]:
    """Returns the user ID and password from the PIN."""

    if len(pin) < 6:
        raise ValueError('PIN too short.')

    return b62decode(pin[:2]), pin[4:]


def encode_pin(uid: int, passwd: str) -> str:
    """Encodes a user ID and a password into a PIN."""

    if len(uid := b62encode(uid).ljust(2, '0')) != 2:
        raise ValueError('Cannot b62encode UID:', uid)

    return uid + passwd
