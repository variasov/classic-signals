from typing import Union

import pytest

from classic.components import component
from classic.signals import signal, Hub, reaction


@signal
class SomeSignal:
    some_field: int


@signal
class AnotherSignal:
    some_field: int


@component
class SomeHandlers:
    hub: Hub

    def __init__(self):
        self.hub.register(self)

    @reaction
    def assign_1(self, signal_: SomeSignal):
        signal_.some_field = 1

    @reaction
    def assign_2(self, signal_: AnotherSignal):
        signal_.some_field = 2


class AnotherHandlers:

    def assign_3(self, event: Union[SomeEvent, AnotherEvent]):
        event.some_field = 3


@component
class SomeService:
    hub: Hub

    def do(self):
        self.hub.notify(SomeSignal())


@pytest.fixture
def hub():
    return Hub()


@pytest.fixture
def some_handlers():
    return SomeHandlers()


@pytest.fixture
def another_handlers():
    return AnotherHandlers()


@pytest.fixture
def some_event():
    return SomeEvent(0)


@pytest.fixture
def another_event():
    return AnotherEvent(0)


def test_define_events(event):
    assert isinstance(event, Event)
    assert isinstance(event, SomeEvent)
    assert hasattr(event, 'some_field')
    assert event.some_field == 0


def test_simple_events_handling(hub, some_handlers, some_event, another_event):
    hub.add_handlers(some_handlers)
    hub.notify(some_event, another_event)

    assert some_event.some_field == 1
    assert another_event.some_field == 2


def test_complex_events_handling_with_many_handlers(
    hub, some_handlers, another_handlers,
    some_event, another_event
):
    hub.add_handlers(some_handlers, another_handlers)
    hub.notify(some_event, another_event)

    assert some_event.some_field == 3
    assert another_event.some_field == 3


def test_hub_as_ctx_manager(hub, some_handlers, some_event, another_event):
    hub.add_handlers(some_handlers)

    with hub:
        hub.add(some_event, another_event)

    assert some_event.some_field == 1
    assert another_event.some_field == 1


def test_hub_as_ctx_manager_with_exception(hub, some_handlers,
                                           some_event, another_event):
    hub.add_handlers(some_handlers)

    with pytest.raises(ValueError):
        with hub:
            hub.add(some_event, another_event)
            raise ValueError

    assert some_event.some_field == 0
    assert another_event.some_field == 0
    assert len(hub._buffer) == 0


def test_events_handling_in_decorator(hub, some_handlers, some_event):
    hub.add_handlers(some_handlers)
    service = SomeService(event=some_event, events=hub)

    service.do()

    assert some_event.some_field == 1
    assert len(hub._buffer) == 0
