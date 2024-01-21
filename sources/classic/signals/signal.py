from typing import Any, TypeVar, Type, Protocol, runtime_checkable
from dataclasses import dataclass


@runtime_checkable
class Signal(Protocol):
    __is_signal: bool


SignalType = TypeVar('SignalType', bound=Type[Signal])


def signal(cls: SignalType) -> SignalType:
    new_cls = dataclass(cls, eq=False)
    new_cls.__is_signal = True
    return new_cls


def is_signal(obj: Any) -> bool:
    return isinstance(obj, Signal)
