from typing import Any, List, Callable, TypeVar
import inspect

Reaction = TypeVar('Reaction', bound=Callable[[Any], Any])


def is_reaction(obj: Any) -> bool:
    """
    Проверяет, является ли объект реакцией.
    :param obj: объект
    """
    return callable(obj) and getattr(obj, '__is_reaction', False)


def filter_reactions(obj: Any) -> List[Reaction]:
    """
    Возвращает список реакций, определенных в объекте.
    :param obj: объект с реакциями
    """
    return [
        member
        for name, member
        in inspect.getmembers(obj, predicate=is_reaction)
    ]
