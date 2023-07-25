"""Password generation."""

from itertools import islice
from secrets import choice
from string import ascii_letters, digits
from typing import Iterator


__all__ = ["genpw", "random_sequence"]


def genpw(length: int = 16, *, pool: str = ascii_letters + digits) -> str:
    """Generates a password."""

    return "".join(islice(random_sequence(pool), length))


def random_sequence(pool: str) -> Iterator[str]:
    """Generates a random sequence of chars given the pool."""

    while True:
        yield choice(pool)
