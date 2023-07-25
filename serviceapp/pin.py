"""PIN handling."""

from typing import NamedTuple

from basex import decode, encode


__all__ = ["decode_pin", "encode_pin"]


LEGIBLE = "ABCDEFGHJKLMNPRTUVWXYZ" "abcdefghijkmnopqrstuvwxyz" "2346789"


class Credentials(NamedTuple):
    """User login credentials."""

    id: int
    passwd: str


def legible_encode(number: int) -> str:
    """Base62 encodes a non-negative integer."""

    return "".join(reversed(encode(number, pool=LEGIBLE)))


def legible_decode(code: str) -> int:
    """Base62-decodes a non-negative integer."""

    return decode("".join(reversed(code)), pool=LEGIBLE)


def decode_pin(pin: str, *, pw_len: int = 4) -> Credentials:
    """Returns the user ID and password from the PIN."""

    if (pin_len := len(pin)) <= pw_len:
        raise ValueError("PIN too short.")

    id_len = pin_len - pw_len
    return Credentials(legible_decode(pin[:id_len]), pin[id_len:])


def encode_pin(uid: int, passwd: str, *, id_max_size: int = 2) -> str:
    """Encodes a user ID and a password into a PIN."""

    if len(uid := legible_encode(uid)) > id_max_size:
        raise ValueError(f"Cannot encode UID {uid} with {id_max_size} digits.")

    return uid + passwd
