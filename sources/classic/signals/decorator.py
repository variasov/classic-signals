from classic.components import add_extra_annotation

from .reaction import ReactionType
from .hub import Hub


def reaction(fn: ReactionType) -> ReactionType:
    add_extra_annotation(fn, 'signals', Hub)
    fn.__is_reaction = True
    return fn
