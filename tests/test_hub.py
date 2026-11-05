"""Тесты хаба сигналов."""

import threading
from dataclasses import dataclass

from classic.signals import Hub


@dataclass
class SomeSignal:
    """Пример сигнала."""

    value: int


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
