
def check_all_reaction_called(handlers, some_signal, another_signal):
    assert handlers.some_field is None
    assert handlers.another_field is None

    hub = handlers.hub
    hub.notify(some_signal)
    hub.notify(another_signal)

    assert handlers.some_field == some_signal
    assert handlers.another_field == another_signal


def check_nothing_is_called(handlers, some_signal, another_signal):
    assert handlers.some_field is None
    assert handlers.another_field is None

    hub = handlers.hub
    hub.notify(some_signal)
    hub.notify(another_signal)

    assert handlers.some_field is None
    assert handlers.another_field is None


def test_composite_handlers(component_handlers, some_signal, another_signal):
    check_all_reaction_called(component_handlers, some_signal, another_signal)


def test_manual_handlers_call_after_registration(
    manual_handlers, some_signal, another_signal
):
    manual_handlers.register()
    check_all_reaction_called(manual_handlers, some_signal, another_signal)
    manual_handlers.unregister()


def test_manual_handlers_dont_call_without_registration(
    manual_handlers, some_signal, another_signal
):
    check_nothing_is_called(manual_handlers, some_signal, another_signal)


def test_manual_handlers_dont_call_after_deregistration(
    manual_handlers, some_signal, another_signal
):
    manual_handlers.register()
    manual_handlers.unregister()
    check_nothing_is_called(manual_handlers, some_signal, another_signal)


def test_manual_handlers_call_after_manual_registration(
    manual_handlers, some_signal, another_signal
):
    manual_handlers.register_manually()
    check_all_reaction_called(manual_handlers, some_signal, another_signal)
    manual_handlers.unregister_manually()


def test_manual_handlers_dont_call_without_manual_registration(
    manual_handlers, some_signal, another_signal
):
    check_nothing_is_called(manual_handlers, some_signal, another_signal)


def test_manual_handlers_dont_call_after_manual_deregistration(
    manual_handlers, some_signal, another_signal
):
    manual_handlers.register_manually()
    manual_handlers.unregister_manually()
    check_nothing_is_called(manual_handlers, some_signal, another_signal)


def test_manual_handlers_call_after_manual_registration_without_signals(
    manual_handlers, some_signal, another_signal
):
    manual_handlers.register_manually_without_signals()
    check_all_reaction_called(manual_handlers, some_signal, another_signal)
    manual_handlers.unregister_manually_without_signals()


def test_manual_handlers_dont_call_without_manual_registration_without_signals(
    manual_handlers, some_signal, another_signal
):
    check_nothing_is_called(manual_handlers, some_signal, another_signal)


def test_manual_handlers_dont_call_after_manual_deregistration_without_signals(
    manual_handlers, some_signal, another_signal
):
    manual_handlers.register_manually_without_signals()
    manual_handlers.unregister_manually_without_signals()
    check_nothing_is_called(manual_handlers, some_signal, another_signal)
