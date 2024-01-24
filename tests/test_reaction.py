from classic.signals import Hub, is_reaction, filter_reactions


def test_is_reaction_true(handlers):
    assert is_reaction(handlers.reaction_1)


def test_is_reaction_false(handlers):
    assert not is_reaction(handlers.reaction_3)


def test_filter_reactions(handlers):
    reactions = filter_reactions(handlers)
    assert len(reactions) == 2


def test_reaction_decorator(handlers):
    assert getattr(handlers.reaction_1, '__is_reaction', False)
    assert getattr(
        handlers.reaction_1,
        '__extra_annotations__',
    ) == {'hub': Hub}
