from functools import wraps
import inspect
from typing import Any, List, TypeVar

from classic.components import add_annotation

from .signal import Reaction
from .hub import Hub


T = TypeVar('T')


def is_watcher(fn: Any) -> bool:
    return callable(fn) and getattr(fn, '__is_watcher', False)


def get_watchers(obj: Any) -> List[Reaction]:
    return [
        member
        for name, member
        in inspect.getmembers(obj, predicate=is_watcher)
    ]


def watch_signal(fn: T) -> T:
    add_annotation(fn, 'signals', Hub)
    fn.__is_watcher = True
    return fn


def _patch_init(cls: T) -> T:
    original_init = getattr(cls, '__init__', None)

    @wraps(original_init)
    def __init__(self, *args, **kwargs):
        original_init(self, *args, **kwargs)

        self._watchers = get_watchers(self)
        for watcher_ in self._watchers:
            self.signals.add_watcher(watcher_)

    cls.__init__ = __init__

    return cls


def _patch_del(cls: T) -> T:
    original_del = getattr(cls, '__del__', None)

    @wraps(original_del)
    def __del__(self):
        for watcher_ in self._watchers:
            self.signals.remove_watcher(watcher_)
        if original_del:
            original_del()

    cls.__del__ = __del__

    return cls


def watcher(cls: T) -> T:
    _patch_init(cls)
    _patch_del(cls)
    return cls
