class SomeSignal:
    __is_signal: bool = False


def test_signal_decorator(some_signal):
    assert hasattr(some_signal, '__is_signal')


def test_signal_protocol():
    some_signal = SomeSignal()
    assert hasattr(some_signal, '_SomeSignal__is_signal')
