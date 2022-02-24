"""PIN handling."""

from functools import partial
from string import digits, ascii_letters

from basex import decode, encode


__all__ = ['decode_pin', 'encode_pin']


b62encode = partial(encode, pool=digits+ascii_letters)
b62decode = partial(decode, pool=digits+ascii_letters)


def decode_pin(pin: str, *, id_size: int = 2) -> tuple[int, str]:
    """Returns the user ID and password from the PIN."""

    if len(pin) <= id_size:
        raise ValueError('PIN too short.')

    return b62decode(pin[:id_size]), pin[id_size:]


def encode_pin(uid: int, passwd: str, *, id_size: int = 2) -> str:
    """Encodes a user ID and a password into a PIN."""

    if len(uid := b62encode(uid).ljust(id_size, '0')) != id_size:
        raise ValueError('Cannot b62encode UID:', uid)

    return uid + passwd
