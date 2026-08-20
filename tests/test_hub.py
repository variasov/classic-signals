from dataclasses import dataclass

from classic.signals import Hub


@dataclass
class SomeSignal:
    value: int


@dataclass
class Handlers:
    hub: Hub
    result: int = 0

    def __post_init__(self):
        self.hub.add_reaction(
            SomeSignal, self.on_some_signal,
        )
        self.result = 0

    def on_some_signal(self, signal: SomeSignal):
        self.result += signal.value


def test_hub():
    hub = Hub()
    handlers = Handlers(hub=hub)

    signal = SomeSignal(value=1)

    hub.notify(signal)

    assert hub._reactions[SomeSignal] == [handlers.on_some_signal]
    assert handlers.result == 1
