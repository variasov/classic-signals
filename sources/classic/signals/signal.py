from typing import Any, TypeVar
from dataclasses import dataclass


Signal = TypeVar('Signal')


def signal(cls: Signal) -> Signal:
    new_cls = dataclass(cls, eq=False, frozen=True)
    new_cls.__is_signal = True
    return new_cls


def is_signal(obj: Any) -> bool:
    return hasattr(obj, '__is_signal')
