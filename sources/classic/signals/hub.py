"""Хаб сигналов: привязка реакций к сигналам и их вызов."""

from collections import defaultdict
from contextlib import suppress

from readerwriterlock import rwlock

from .types import Reaction, Signal


class Hub:
    """Хранит знания о сигналах и привязанных к ним реакциям.

    Принимает сигналы и инициирует реакции на сигналы.

    Реакции вызываются внутри notify, пока хаб удерживает блокировку
    чтения, поэтому вызывать add_reaction или remove_reaction из
    реакций нельзя: это приведёт к взаимоблокировке.
    """

    _reactions: dict[type[Signal], list[Reaction]]
    _lock: rwlock.RWLockRead

    def __init__(self) -> None:
        """Создаёт пустой хаб без зарегистрированных реакций."""
        self._reactions = defaultdict(list)
        self._lock = rwlock.RWLockRead()

    def notify(self, *signals: Signal) -> None:
        """Вызывает зарегистрированные реакции для указанных сигналов.

        Реакции вызываются последовательно в текущем потоке в порядке
        регистрации. Диспетчеризация по точному классу сигнала: реакция,
        зарегистрированная на базовый класс, не вызывается для
        сигналов-наследников. Исключение, брошенное реакцией,
        прерывает оставшиеся реакции и пробрасывается вызывающему коду.

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

        Нельзя вызывать из реакции: это приведёт к взаимоблокировке.

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

        Нельзя вызывать из реакции: это приведёт к взаимоблокировке.

        :param signal: Класс сигнала, на который должна реагировать реакция.
        :param reaction: Вызываемый объект с одним аргументом - сигналом.
        """
        with self._lock.gen_wlock(), suppress(ValueError):
            self._reactions[signal].remove(reaction)
