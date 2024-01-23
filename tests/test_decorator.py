from classic.signals import Hub


def test_reaction_decorator(some_handlers):
    assert 'signals' in some_handlers.__annotations__
    assert some_handlers.__annotations__['signals'] == Hub
    assert getattr(some_handlers.assign_1, '__is_reaction', False)
