from dataclasses import is_dataclass

from classic.signals import is_signal


class SomeClass:
    pass


def test_signal_decorator(some_signal):
    assert hasattr(some_signal, '__is_signal')
    assert is_dataclass(some_signal)


def test_is_signal_true(some_signal):
    assert is_signal(some_signal)


def test_is_signal_false():
    some_class = SomeClass()
    assert not is_signal(some_class)
