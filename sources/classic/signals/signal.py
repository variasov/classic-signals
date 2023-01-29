from typing import Callable, TypeVar, Type
from dataclasses import dataclass


AnyClass = TypeVar('AnyClass')


class Signal:
    pass


Reaction = Callable[[Signal], None]


def signal(cls: Type[object]) -> Type[Signal]:
    bases = (Signal,) + cls.__bases__
    new_cls = type(cls.__name__, bases, dict(cls.__dict__))
    return dataclass(new_cls)
