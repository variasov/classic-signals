# Classic Signals

Библиотека предоставляет просую реализацию паттерна Observer для инверсии контроля через сигналы и реакции.

Потокобезопасно.

В одном месте программы мы объявляем сигналы, пользуясь декоратором signal, в других местах приложения пишем реакции на этих сигналов. Реакции - это любой вызываемый объект, принимающий один аргумент - инстанс сигнала. Это может быть и просто функция или метод. Последнее, что нужно, это инстанс класса Hub. В Hub перед началом работы можно зарегистрировать реакции, потом можно вызвать у него метод notify, передав в него инстанс сигнала, и Hub вызовет все реакции, относящиеся к сигналу.

Реакции исполняются последовательно в единственном текущем потоке.
Не рекомендуется создавать новые потоки из сигналов. Этот механизм предназначается для связки разных частей кода с инверсией зависимости, не для распараллеливания задач.

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
    
    def on_something_another_happened(self, signal: SomethingAnotherHappened):
        print(f'Что-то еще произошло: {signal}')


hub = Hub()
SomeHandlers(hub=hub)

signal_1 = SomethingHappened(some_field=0)
signal_2 = SomethingAnotherHappened(some_field=0)

hub.notify(signal_1, signal_2)
```
