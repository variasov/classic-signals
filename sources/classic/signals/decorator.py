from classic.components import add_extra_annotation

from .hub import Hub
from .reaction import Reaction


def reaction(fn: Reaction) -> Reaction:
    """
    Декоратор для маркировки функции как реакции.
    :param fn: функция реакции
    :return: та же самая функция реакции
    """
    add_extra_annotation(fn, 'hub', Hub)
    fn.__is_reaction = True
    return fn
