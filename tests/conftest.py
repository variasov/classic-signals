from pytest import fixture

from classic.components import component
from classic.signals import signal, reaction, Hub


@signal
class SomeSignal:
    some_field: int


@signal
class AnotherSignal:
    some_field: int


class Handlers:
    some_field: SomeSignal = None
    another_field: AnotherSignal = None

    @reaction
    def reaction_1(self, signal_: SomeSignal):
        self.some_field = signal_

    @reaction
    def reaction_2(self, signal_: AnotherSignal):
        self.another_field = signal_

    def reaction_3(self):
        ...


class HandlersManual(Handlers):

    def __init__(self, hub: Hub):
        self.some_field = None
        self.another_field = None
        self.hub = hub

    def register(self):
        self.hub.register(self)

    def unregister(self):
        self.hub.unregister(self)

    def register_manually(self):
        self.hub.add_reaction(self.reaction_1, SomeSignal)
        self.hub.add_reaction(self.reaction_2, AnotherSignal)

    def unregister_manually(self):
        self.hub.remove_reaction(self.reaction_1, SomeSignal)
        self.hub.remove_reaction(self.reaction_2, AnotherSignal)

    def register_manually_without_signals(self):
        self.hub.add_reaction(self.reaction_1)
        self.hub.add_reaction(self.reaction_2)

    def unregister_manually_without_signals(self):
        self.hub.remove_reaction(self.reaction_1)
        self.hub.remove_reaction(self.reaction_2)


@component
class HandlersComponent(Handlers):
    pass


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
def component_handlers(hub):
    return HandlersComponent(hub=hub)


@fixture
def manual_handlers(hub):
    return HandlersManual(hub=hub)


@fixture
def handlers(hub):
    handlers = HandlersManual(hub=hub)
    handlers.register()
    yield handlers
    handlers.unregister()
