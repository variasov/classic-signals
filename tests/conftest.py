from pytest import fixture

from classic.components import component
from classic.signals import signal, reaction, Hub


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

    def assign_3(self):
        ...


@fixture
def some_signal():
    return SomeSignal(some_field=0)


@fixture
def another_signal():
    return AnotherSignal(some_field=0)


@fixture
def hub():
    return Hub()


@fixture
def hub_2():
    """
    2й хаб для тестов, где нужно проверить ручной вызов публичных методов. 
    Первыйх хаб используется для инита SomeHandlers и автоматически проводит 
    регистрацию, поэтому не подходит нам.
    """""
    return Hub()


@fixture
def some_handlers(hub):
    return SomeHandlers(signals=hub)
