"""Configuration file loading."""

from functools import partial
from pathlib import Path

from configlib import load_config


__all__ = ["get_oauth2"]


OAUTH2_JSON = Path("/usr/local/etc/comcat.d/oauth2.json")

get_oauth2 = partial(load_config, OAUTH2_JSON)
