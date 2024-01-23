from classic.components import add_extra_annotation

from .hub import Hub
from .reaction import Reaction


def reaction(fn: Reaction) -> Reaction:
    add_extra_annotation(fn, 'signals', Hub)
    fn.__is_reaction = True
    return fn
