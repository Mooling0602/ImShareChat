import re

from typing import Callable, Any
from mcdreforged.api.all import *


def extract_file(server: PluginServerInterface, file_path, target_path):
    with server.open_bundled_file(file_path) as file_handler:
        with open(target_path, 'wb') as target_file:
            target_file.write(file_handler.read())

# Usage: @execute_if(bool | Callable -> bool)
def execute_if(condition: bool | Callable[[], bool]):
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            actual_condition = condition() if callable(condition) else condition
            if actual_condition:
                return func(*args, **kwargs)
            return None
        return wrapper
    return decorator

def remove_format_codes(text):
    # 正则表达式匹配所有以§开头的格式化代码
    return re.sub(r'§[0-9a-fA-Fk-oK-OrRg-tz]', '', text)