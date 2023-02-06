from functools import partial
from typing import Any, Type, List, Dict, Deque, Optional
import threading
from collections import defaultdict, deque
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
    _storage: threading.local = field(
        init=False, default_factory=threading.local,
    )

    @property
    def _buffer(self) -> Deque[Signal]:
        if not hasattr(self._storage, 'buffer'):
            self._storage.buffer = deque()
        return self._storage.buffer

    def notify_deferred(self) -> None:
        buffer = self._buffer
        while buffer:
            signal = buffer.popleft()
            self.notify(signal)

    def reset_deferred(self) -> None:
        self._buffer.clear()

    def defer(self, *signals: Signal):
        self._buffer.extend(signals)

    def notify(self, *signals: Signal) -> None:
        with threading.Lock():
            for signal in signals:
                for reaction in self._reactions[signal.__class__]:
                    reaction(signal)

    def add_reaction(
        self,
        reaction: Reaction,
        signal: Optional[Type[Signal]] = None,
    ):
        signal = signal or utils.get_signal_type(reaction)
        with threading.Lock():
            if reaction not in self._reactions[signal]:
                self._reactions[signal].append(reaction)

    def remove_reaction(self, reaction: Reaction):
        with threading.Lock():
            for reactions in self._reactions.values():
                reactions.remove(reaction)

    @staticmethod
    def is_reaction(fn: Any) -> bool:
        return callable(fn) and getattr(fn, '__is_reaction', False)

    @classmethod
    def get_reactions(cls, obj: Any) -> List[Reaction]:
        return [
            member
            for name, member
            in inspect.getmembers(obj, predicate=cls.is_reaction)
        ]

    def register(self, obj: Any) -> None:
        reactions = self.get_reactions(obj)
        for reaction in reactions:
            self.add_reaction(reaction)

    def unregister(self, obj: Any) -> None:
        reactions = self.get_reactions(obj)
        for reaction in reactions:
            self.remove_reaction(reaction)
