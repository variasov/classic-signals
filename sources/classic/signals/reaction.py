import inspect
from typing import Any, List, TypeVar

from classic.components import add_self_annotation

from .signal import Reaction
from .hub import Hub


T = TypeVar('T')


def reaction(fn: T) -> T:
    add_self_annotation(fn, 'signals', Hub)
    fn.__is_reaction = True
    return fn
