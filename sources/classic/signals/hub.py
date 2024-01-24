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
    """
    Хаб это центральная точка коммуникации между реакциями и сигналами.
    Он хранит реестр всех реакций и соответствующих им сигналов.
    """

    _reactions: dict[Signal, list[Reaction]]
    _lock: rwlock.RWLockRead


    def __init__(self):
        self._reactions = defaultdict(list)
        self._lock = rwlock.RWLockRead(threading.RLock)

    def notify(self, *signals: Signal) -> None:
        """
        Вызывает зарегистрированные реакции для заданных сигналов.
        :param signals: сигналы, на которые требуется среагировать
        """
        with self._lock.gen_rlock():
            for signal in signals:
                for reaction in self._reactions[signal.__class__]:
                    reaction(signal)

    def add_reaction(
        self, reaction: Reaction,
        signal: Optional[Type[Signal]] = None,
    ) -> None:
        """
        Добавить реакцию в реестр.
        :param reaction: функция реакции
        """
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
        """
        Удалить реакцию из реестра.
        :param reaction: функция реакции
        """
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
        """
        Регистрирует все реакции, определенные в объекте.
        :param obj: объект, содержащий реакции
        """
        with self._lock.gen_wlock():
            for reaction in filter_reactions(obj):
                self.add_reaction(reaction)

    def unregister(self, obj: Any) -> None:
        """
        Удаляет все реакции, определенные в объекте.
        :param obj: объект, содержащий реакции
        """
        with self._lock.gen_wlock():
            for reaction in filter_reactions(obj):
                self.remove_reaction(reaction)
