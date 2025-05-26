"""Utils for plugin.
"""
import re

from typing import Callable, TypeVar, ParamSpec
from functools import wraps
from mcdreforged.api.all import ServerInterface, PluginServerInterface


psi = ServerInterface.psi()


def extract_file(server: PluginServerInterface, file_path: str, target_path: str):
    """Extract file from plugin pack.
    """
    with server.open_bundled_file(file_path) as file_handler:
        with open(target_path, 'wb') as target_file:
            target_file.write(file_handler.read())


# Usage: @execute_if(lambda: bool | Callable -> bool)
P = ParamSpec("P")
R = TypeVar("R")

def execute_if(condition: bool | Callable[[], bool]) \
    -> Callable[[Callable[P, R]], Callable[P, R | None]]:
    """A decorator to preset conditions before execute a function.
    """
    def decorator(func: Callable[P, R]) -> Callable[P, R | None]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
            actual_condition = condition() if callable(condition) else condition
            if actual_condition:
                return func(*args, **kwargs)
            return None
        return wrapper
    return decorator

def remove_format_codes(text: str) -> str:
    """Remove MC color codes.
    """
    return re.sub(r'§[0-9a-fA-Fk-oK-OrRg-tz]', '', text)
