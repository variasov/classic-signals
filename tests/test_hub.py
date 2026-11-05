"""Тесты хаба сигналов."""

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
