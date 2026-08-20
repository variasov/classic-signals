from collections.abc import Callable
from typing import Any

Signal = Any
Reaction = Callable[[Signal], Any]
