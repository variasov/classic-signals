"""Хаб сигналов: привязка реакций к сигналам и их вызов."""

import threading
from collections import defaultdict
from contextlib import suppress

from readerwriterlock import rwlock

from .types import Reaction, Signal


class Hub:
    """Хранит знания о сигналах и привязанных к ним реакциям.

    Принимает сигналы и инициирует реакции на сигналы.
    """

    _reactions: dict[type[Signal], list[Reaction]]
    _lock: rwlock.RWLockRead

    def __init__(self) -> None:
        """Создаёт пустой хаб без зарегистрированных реакций."""
        self._reactions = defaultdict(list)
        self._lock = rwlock.RWLockRead(threading.RLock)

    def notify(self, *signals: Signal) -> None:
        """Вызывает зарегистрированные реакции для указанных сигналов.

        :param signals: Сигналы, на которые требуется среагировать.
        """
        with self._lock.gen_rlock():
            for signal in signals:
                for reaction in self._reactions[signal.__class__]:
                    reaction(signal)

    def add_reaction(
        self,
        signal: type[Signal],
        reaction: Reaction,
    ) -> None:
        """Добавляет реакцию на сигнал.

        :param signal: Класс сигнала, на который должна реагировать реакция.
        :param reaction: Вызываемый объект с одним аргументом - сигналом.
        """
        with self._lock.gen_wlock():
            if reaction not in self._reactions[signal]:
                self._reactions[signal].append(reaction)

    def remove_reaction(
        self,
        signal: type[Signal],
        reaction: Reaction,
    ) -> None:
        """Убирает реакцию на сигнал.

        :param signal: Класс сигнала, на который должна реагировать реакция.
        :param reaction: Вызываемый объект с одним аргументом - сигналом.
        """
        with self._lock.gen_wlock(), suppress(ValueError):
            self._reactions[signal].remove(reaction)
