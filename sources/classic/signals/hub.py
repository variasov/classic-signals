from typing import Any, Optional
import threading
from collections import defaultdict
from typing import Type

from classic.components import Registry
from readerwriterlock import rwlock

from .reaction import filter_reactions, Reaction
from .signal import Signal
from . import utils


class Hub(Registry):
    _reactions: dict[Signal, list[Reaction]]
    _lock: rwlock.RWLockRead

    def __init__(self):
        self._reactions = defaultdict(list)
        self._lock = rwlock.RWLockRead(threading.RLock)

    def notify(self, *signals: Signal) -> None:
        with self._lock.gen_rlock():
            for signal in signals:
                for reaction in self._reactions[signal.__class__]:
                    reaction(signal)

    def add_reaction(
        self, reaction: Reaction,
        signal: Optional[Type[Signal]] = None,
    ) -> None:
        signal = signal or utils.get_signal_type(reaction)
        with self._lock.gen_wlock():
            if reaction not in self._reactions[signal]:
                self._reactions[signal].append(reaction)

    @staticmethod
    def _remove_reaction(reactions: list[Reaction], reaction: Reaction) -> None:
        try:
            reactions.remove(reaction)
        except (KeyError, ValueError):
            pass

    def remove_reaction(
        self, reaction: Reaction,
        signal: Optional[Type[Signal]] = None,
    ) -> None:
        with self._lock.gen_wlock():
            if signal:
                try:
                    self._reactions[signal].remove(reaction)
                except ValueError:
                    pass
            else:
                for reactions in self._reactions.values():
                    try:
                        self._remove_reaction(reactions, reaction)
                    except ValueError:
                        pass

    def register(self, obj: Any) -> None:
        with self._lock.gen_wlock():
            for reaction in filter_reactions(obj):
                self.add_reaction(reaction)

    def unregister(self, obj: Any) -> None:
        with self._lock.gen_wlock():
            for reaction in filter_reactions(obj):
                self.remove_reaction(reaction)
