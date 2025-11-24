from os import getenv


def get_env_or_throw(name: str) -> str:
    value = getenv(name)
    if value is None:
        raise EnvironmentError(f"{name} is not set")
    return value
