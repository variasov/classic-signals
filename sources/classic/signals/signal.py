from typing import Any, TypeVar
from dataclasses import dataclass


Signal = TypeVar('Signal')


def signal(cls: Signal) -> Signal:
    """
    Декоратор, помечающий класс как сигнал.
    :param cls: класс сигнала
    """
    new_cls = dataclass(cls, eq=False, frozen=True)
    new_cls.__is_signal = True
    return new_cls


def is_signal(obj: Any) -> bool:
    """
    Проверяет, является ли объект сигналом.
    :param obj: объект для проверки
    """
    return hasattr(obj, '__is_signal')
