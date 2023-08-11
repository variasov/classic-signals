from typing import Any, Callable, TypeVar

from classic.components import add_extra_annotation

from .hub import Hub


T = TypeVar('T', bound=Callable[[Any], Any])


def reaction(fn: T) -> T:
    add_extra_annotation(fn, 'signals', Hub)
    fn.__is_reaction = True
    return fn
