# Classic Signals

This package provides primitives for signal handling.
Part of project "Classic".

Usage:

```python
from classic.components import component
from classic.signals import reaction, Hub, signal


@signal
class SomeSignal:
    some_field: int


@signal
class AnotherSignal:
    some_field: int


@component
class SomeHandlers:

    @reaction
    def assign_1(self, signal_: SomeSignal):
        signal_.some_field = 1

    @reaction
    def assign_2(self, signal_: AnotherSignal):
        signal_.some_field = 2


hub = Hub()
SomeHandlers(signals=hub)

some_signal = SomeSignal(some_field=0)
another_signal = AnotherSignal(some_field=0)
hub.notify(some_signal)
hub.notify(another_signal)

# >>> some_signal.some_field
#     1
# >>> another_signal.some_field
#     2
```