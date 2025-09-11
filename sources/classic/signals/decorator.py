from classic.components import add_extra_annotation

from .hub import Hub
from .reaction import Reaction


def reaction(fn: Reaction) -> Reaction:
    """
    Декоратор, помечающий указанную функцию,
    как реакцию на сигнал, чтобы затем Hub автоматически их регистрировал.

    :param fn: функция
    :return: та же самая функция
    """
    add_extra_annotation(fn, 'hub', Hub)
    fn.__is_reaction = True
    return fn
