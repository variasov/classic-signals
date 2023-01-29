from functools import partial
from typing import Type, List, Dict, Deque, Optional
import threading
from collections import defaultdict, deque

import attr
from classic.components import component

from .signal import Signal, Reaction
from . import _utils


@component
class Hub:

    _reactions: Dict[
        Type[Signal], List[Reaction]
    ] = attr.ib(init=False, factory=partial(defaultdict, list))

    _storage: threading.local = attr.ib(init=False, factory=threading.local)

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
        for signal in signals:
            for reaction in self._reactions[signal.__class__]:
                reaction(signal)

    def add_watcher(
        self,
        reaction: Reaction,
        signal: Optional[Type[Signal]] = None,
    ):
        signal = signal or _utils.get_event_type(reaction)
        with threading.Lock():
            if reaction not in self._reactions[signal]:
                self._reactions[signal].append(reaction)

    def remove_watcher(self, reaction: Reaction):
        with threading.Lock():
            for reactions in self._reactions.values():
                reactions.remove(reaction)
