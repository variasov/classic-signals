from classic.signals import is_reaction, filter_reactions


def test_is_reaction_true(some_handlers):
    assert is_reaction(some_handlers.assign_1)


def test_is_reaction_false(some_handlers):
    assert not is_reaction(some_handlers.assign_3)


def test_filter_reactions(some_handlers):
    reactions = filter_reactions(some_handlers)
    assert len(reactions) == 2
