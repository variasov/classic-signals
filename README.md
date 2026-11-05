# Classic Signals

Библиотека предоставляет простую реализацию паттерна Observer для инверсии контроля через сигналы и реакции.

Потокобезопасно.

В одном месте программы мы объявляем сигналы, в других местах приложения пишем реакции на эти сигналы. Реакции - это любой вызываемый объект, принимающий один аргумент - инстанс сигнала. Это может быть и просто функция или метод. Последнее, что нужно, это инстанс класса Hub. В Hub перед началом работы можно зарегистрировать реакции, потом можно вызвать у него метод notify, передав в него инстанс сигнала, и Hub вызовет все реакции, относящиеся к сигналу.

Семантика:

- Реакции исполняются последовательно в текущем потоке в порядке регистрации.
- Диспетчеризация по точному классу сигнала: реакция, зарегистрированная на базовый класс, не вызывается для сигналов-наследников.
- Исключение, брошенное реакцией, прерывает оставшиеся реакции и пробрасывается вызывающему коду notify.
- Реакции вызываются внутри notify под блокировкой чтения, поэтому вызывать add_reaction или remove_reaction из реакций нельзя: это приведёт к взаимоблокировке.
- Не рекомендуется создавать новые потоки из сигналов. Этот механизм предназначается для связки разных частей кода с инверсией зависимости, не для распараллеливания задач.

Пример:

```python
from dataclasses import dataclass

from classic.signals import Hub


@dataclass
class SomethingHappened:
    some_field: int


@dataclass
class SomethingAnotherHappened:
    some_field: int


@dataclass
class SomeHandlers:
    hub: Hub

    def __post_init__(self):
        self.hub.add_reaction(
            SomethingHappened,
            self.on_something_happened,
        )
        self.hub.add_reaction(
            SomethingAnotherHappened,
            self.on_something_another_happened,
        )

    def on_something_happened(self, signal: SomethingHappened):
        print(f'Что-то произошло: {signal}')

    def on_something_another_happened(
        self,
        signal: SomethingAnotherHappened,
    ):
        print(f'Что-то еще произошло: {signal}')


hub = Hub()
SomeHandlers(hub=hub)

signal_1 = SomethingHappened(some_field=0)
signal_2 = SomethingAnotherHappened(some_field=0)

hub.notify(signal_1, signal_2)
```
