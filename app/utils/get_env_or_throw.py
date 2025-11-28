from collections.abc import Callable
from os import getenv

from annotated_types import T


def get_env_or_throw(name: str, cast: Callable[[str], T] = str) -> T:
    value = getenv(name)
    if value is None:
        raise EnvironmentError(f"{name} is not set")
    return cast(value)
