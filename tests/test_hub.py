def test_register(some_handlers, some_signal, another_signal, hub_2):
    hub_2.register(some_handlers)

    assert hub_2._reactions[some_signal.__class__] == [some_handlers.assign_1]
    assert hub_2._reactions[another_signal.__class__] == (
        [some_handlers.assign_2]
    )
    assert len(hub_2._reactions) == 2


def test_unregister(some_handlers, hub_2, some_signal, another_signal):
    hub_2.register(some_handlers)
    hub_2.unregister(some_handlers)

    assert hub_2._reactions[some_signal.__class__] == []
    assert hub_2._reactions[another_signal.__class__] == []


def test_notify(some_handlers, some_signal, another_signal):
    hub = some_handlers.signals
    hub.notify(some_signal)
    hub.notify(another_signal)

    assert some_signal.some_field == 1
    assert another_signal.some_field == 2
