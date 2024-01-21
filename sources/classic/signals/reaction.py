from typing import Any, TypeVar, List, Protocol, runtime_checkable
import inspect

from .signal import Signal


@runtime_checkable
class Reaction(Protocol):

    def __call__(self, signal: Signal) -> None:
        raise NotImplemented


ReactionType = TypeVar('ReactionType', bound=Reaction)


def is_reaction(obj: Any) -> bool:
    return callable(obj) and getattr(obj, '__is_reaction', False)


def filter_reactions(obj: Any) -> List[Reaction]:
    return [
        member
        for name, member
        in inspect.getmembers(obj, predicate=is_reaction)
    ]
