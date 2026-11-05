"""Тесты хаба сигналов."""

import threading
from dataclasses import dataclass

import pytest
from classic.signals import Hub


@dataclass
class SomeSignal:
    """Пример сигнала."""

    value: int


@dataclass
class OtherSignal:
    """Другой сигнал."""

    value: int


@dataclass
class ChildSignal(SomeSignal):
    """Наследник сигнала для проверки точной диспетчеризации."""


@dataclass
class Handlers:
    """Пример обработчиков, подписывающихся на сигнал."""

    hub: Hub
    result: int = 0

    def __post_init__(self):
        """Подписывает реакции при создании обработчика."""
        self.hub.add_reaction(
            SomeSignal,
            self.on_some_signal,
        )
        self.result = 0

    def on_some_signal(self, signal: SomeSignal):
        """Накапливает значение из сигнала."""
        self.result += signal.value


def test_hub():
    """Реакция регистрируется и вызывается при уведомлении."""
    hub = Hub()
    handlers = Handlers(hub=hub)

    signal = SomeSignal(value=1)

    hub.notify(signal)

    assert hub._reactions[SomeSignal] == [handlers.on_some_signal]
    assert handlers.result == 1


def test_hub_thread_safety():
    """Параллельные notify и add/remove без нарушений не зависают."""
    hub = Hub()
    delivered: list[int] = []
    iterations = 100

    def permanent_reaction(signal: SomeSignal) -> None:
        delivered.append(signal.value)

    def transient_reaction(signal: SomeSignal) -> None:
        pass

    hub.add_reaction(SomeSignal, permanent_reaction)

    def notify_loop() -> None:
        for _ in range(iterations):
            hub.notify(SomeSignal(value=1))

    def subscribe_loop() -> None:
        for _ in range(iterations):
            hub.add_reaction(SomeSignal, transient_reaction)
            hub.remove_reaction(SomeSignal, transient_reaction)

    threads = [
        threading.Thread(target=notify_loop, daemon=True),
        threading.Thread(target=notify_loop, daemon=True),
        threading.Thread(target=subscribe_loop, daemon=True),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=10)

    assert all(not thread.is_alive() for thread in threads)
    assert len(delivered) == iterations * 2


def test_add_reaction_ignores_duplicates():
    """Повторная регистрация той же реакции не дублирует её."""
    hub = Hub()
    delivered: list[int] = []

    def reaction(signal: SomeSignal) -> None:
        delivered.append(signal.value)

    hub.add_reaction(SomeSignal, reaction)
    hub.add_reaction(SomeSignal, reaction)

    hub.notify(SomeSignal(value=1))

    assert hub._reactions[SomeSignal] == [reaction]
    assert delivered == [1]


def test_remove_reaction():
    """Удалённая реакция больше не вызывается."""
    hub = Hub()
    delivered: list[int] = []

    def reaction(signal: SomeSignal) -> None:
        delivered.append(signal.value)

    hub.add_reaction(SomeSignal, reaction)
    hub.remove_reaction(SomeSignal, reaction)

    hub.notify(SomeSignal(value=1))

    assert hub._reactions[SomeSignal] == []
    assert delivered == []


def test_remove_reaction_ignores_missing():
    """Удаление отсутствующей реакции не приводит к ошибке."""
    hub = Hub()

    def reaction(signal: SomeSignal) -> None:
        pass

    def other_reaction(signal: SomeSignal) -> None:
        pass

    hub.add_reaction(SomeSignal, reaction)

    hub.remove_reaction(SomeSignal, other_reaction)
    hub.remove_reaction(SomeSignal, reaction)
    hub.remove_reaction(OtherSignal, reaction)

    assert hub._reactions[SomeSignal] == []


def test_notify_multiple_signals_in_order():
    """Сигналы обрабатываются по очереди, реакции в порядке регистрации."""
    hub = Hub()
    calls: list[str] = []

    def first(signal: SomeSignal) -> None:
        calls.append("first")

    def second(signal: SomeSignal) -> None:
        calls.append("second")

    def other(signal: OtherSignal) -> None:
        calls.append("other")

    hub.add_reaction(SomeSignal, first)
    hub.add_reaction(SomeSignal, second)
    hub.add_reaction(OtherSignal, other)

    hub.notify(SomeSignal(value=1), OtherSignal(value=2))

    assert calls == ["first", "second", "other"]


def test_notify_without_subscribers():
    """Уведомление сигнала без подписчиков не приводит к ошибке."""
    hub = Hub()

    hub.notify(SomeSignal(value=1))


def test_notify_dispatch_is_exact_class():
    """Реакция на базовый класс не вызывается для наследников."""
    hub = Hub()
    delivered: list[int] = []

    def reaction(signal: SomeSignal) -> None:
        delivered.append(signal.value)

    hub.add_reaction(SomeSignal, reaction)

    hub.notify(ChildSignal(value=1))

    assert delivered == []


def test_exception_in_reaction_propagates():
    """Исключение реакции обрывает остальные реакции и пробрасывается."""
    hub = Hub()
    calls: list[str] = []

    def failing(signal: SomeSignal) -> None:
        calls.append("failing")
        raise RuntimeError("реакция упала")

    def next_reaction(signal: SomeSignal) -> None:
        calls.append("next")

    hub.add_reaction(SomeSignal, failing)
    hub.add_reaction(SomeSignal, next_reaction)

    with pytest.raises(RuntimeError, match="реакция упала"):
        hub.notify(SomeSignal(value=1))

    assert calls == ["failing"]
