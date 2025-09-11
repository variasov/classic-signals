from typing import Any, List, Callable, TypeVar
import inspect


Reaction = TypeVar('Reaction', bound=Callable[[Any], Any])


def is_reaction(obj: Any) -> bool:
    """
    Проверяет, является ли объект реакцией.

    :param obj: объект
    :returns: bool, True, если указанный объект является реакцией.
    """
    return callable(obj) and getattr(obj, '__is_reaction', False)


def filter_reactions(obj: Any) -> List[Reaction]:
    """
    Возвращает список реакций, определенных в объекте.
    :param obj: Объект с методами, помеченными декоратором reaction.
    """
    return [
        member
        for name, member
        in inspect.getmembers(obj, predicate=is_reaction)
    ]
