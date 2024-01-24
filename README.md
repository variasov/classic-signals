# Classic Signals

Данный пакет предоставляет возможность использовать сигналы и реакции в проекте.

Они нужны для инверсии вызова. По сути, это паттерн Observer и немного сахара 
сверху. В одном месте программы мы объявляем сигналы, пользуясь декоратором 
signal, в других местах приложения пишем реакции на этих сигналов.
Реакции - это любой вызываемый объект, принимающий один аргумент - инстанс 
сигнала. Это может быть и просто функция или метод, для удобства завернутый
в декоратор reaction. Последнее, что нужно, это инстанс класса Hub. В Hub 
перед началом работы можно зарегистрировать реакции, потом можно вызвать у него
метод notify, передав в него инстанс сигнала, и Hub вызовет все реакции, 
относящиеся к сигналу.

Пример:

```python
from classic.components import component
from classic.signals import reaction, Hub, signal


@signal
class SomethingHappened:
    """Под капотом сигналы - на самом деле датаклассы"""
    some_field: int


@signal
class SomethingAnotherHappened:
    some_field: int


@component
class SomeHandlers:

    @reaction
    def on_something_happened(self, signal: SomethingHappened):
        print(f'Что-то произошло: {signal}')

    @reaction
    def on_something_another_happened(self, signal: SomethingAnotherHappened):
        print(f'Что-то еще произошло: {signal}')


hub = Hub()
SomeHandlers(signals=hub)


signal_1 = SomethingHappened(some_field=0)
signal_2 = SomethingAnotherHappened(some_field=0)

hub.notify(signal_1, signal_2)
```


