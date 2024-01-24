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
    Хранит знания о сигналах и привязанных к ним реакциям, принимает сигналы и
    инициирует реакции на сигналы.
    """

    _reactions: dict[Signal, list[Reaction]]
    _lock: rwlock.RWLockRead

    def __init__(self):
        self._reactions = defaultdict(list)
        self._lock = rwlock.RWLockRead(threading.RLock)

    def notify(self, *signals: Signal) -> None:
        """
        Вызывает зарегистрированные реакции для указаных сигналов.

        :param signals: Сигналы, на которые требуется среагировать.
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
        Добавляет реакцию на сигнал.

        Если сигнал не указан, то реакция будет добавлена в сигнал, указанный
        в аннотации вызываемого объекта. Если аннотация не указана, вызовет
        исключение AssertionError.

        Проверка динамическая, построена на assert.

        :param reaction: Вызываемый объект с одним аргументом - сигналом.
        :param signal: Класс сигнала, на который должна реагировать реакция.
        """
        signal = signal or utils.get_signal_type(reaction)
        with self._lock.gen_wlock():
            if reaction not in self._reactions[signal]:
                self._reactions[signal].append(reaction)

    def remove_reaction(
        self, reaction: Reaction,
        signal: Optional[Type[Signal]] = None,
    ) -> None:
        """
        Добавляет реакцию на сигнал.

        Если сигнал не указан, то Hub переберет реакции для всех сигналов,
        и уберет указанный отовсюду.

        :param reaction: Вызываемый объект с одним аргументом - сигналом.
        :param signal: Класс сигнала, на который должна реагировать реакция.
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
                        reactions.remove(reaction)
                    except ValueError:
                        pass

    def register(self, obj: Any) -> None:
        """
        Разбирает указанный объект на реакции, и добавляет их
        к внутреннему реестру.

        Реакцией считается метод, завернутый в декоратор reaction.

        :param obj: Объект, содержащий реакции.
        """
        with self._lock.gen_wlock():
            for reaction in filter_reactions(obj):
                self.add_reaction(reaction)

    def unregister(self, obj: Any) -> None:
        """
        Удаляет все реакции, определенные в объекте.

        Реакцией считается метод, завернутый в декоратор reaction.

        :param obj: Объект, содержащий реакции.
        """
        with self._lock.gen_wlock():
            for reaction in filter_reactions(obj):
                self.remove_reaction(reaction)
