from typing import Any, List, Callable, TypeVar
import inspect

Reaction = TypeVar('Reaction', bound=Callable[[Any], Any])


def is_reaction(obj: Any) -> bool:
    return callable(obj) and getattr(obj, '__is_reaction', False)


def filter_reactions(obj: Any) -> List[Reaction]:
    return [
        member
        for name, member
        in inspect.getmembers(obj, predicate=is_reaction)
    ]
