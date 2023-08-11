from functools import partial
from typing import Any, Type, List, Dict, Optional
import threading
from collections import defaultdict
import inspect

from dataclasses import field
from classic.components import component, Registry

from .signal import Signal, Reaction
from . import utils


@component
class Hub(Registry):

    _reactions: Dict[Type[Signal], List[Reaction]] = field(
        init=False, default_factory=partial(defaultdict, list),
    )
    _lock: threading.Lock = field(
        init=False, default_factory=threading.RLock,
    )

    def notify(self, *signals: Signal) -> None:
        with self._lock.acquire():
            for signal in signals:
                for reaction in self._reactions[signal.__class__]:
                    reaction(signal)

    def add_reaction(
        self,
        reaction: Reaction,
        signal: Optional[Type[Signal]] = None,
    ):
        signal = signal or utils.get_signal_type(reaction)
        with self._lock.acquire():
            if reaction not in self._reactions[signal]:
                self._reactions[signal].append(reaction)

    def remove_reaction(self, reaction: Reaction):
        with self._lock.acquire():
            for reactions in self._reactions.values():
                reactions.remove(reaction)

    @staticmethod
    def is_reaction(fn: Any) -> bool:
        return callable(fn) and getattr(fn, '__is_reaction', False)

    @classmethod
    def filter_reactions(cls, obj: Any) -> List[Reaction]:
        return [
            member
            for name, member
            in inspect.getmembers(obj, predicate=cls.is_reaction)
        ]

    def register(self, obj: Any) -> None:
        with self._lock.acquire():
            for reaction in self.filter_reactions(obj):
                self.add_reaction(reaction)

    def unregister(self, obj: Any) -> None:
        with self._lock.acquire():
            for reaction in self.filter_reactions(obj):
                self.remove_reaction(reaction)
