from typing import Callable, Any
from .data import Arc

class HandleState:
    def __init__(self, init_arc: Callable[[int, int, int, int], Arc], add_arc: Callable[[Arc], Any]) -> None: ...
    def __call__(self, line: str) -> None: ...
