from parsy import *

from scriic.parser.primitives import text, assignment, block


Letters = namedtuple("Letters", "text assign_to steps")


@generate("LETTERS")
def letters():
    assign_to = yield assignment.optional()
    text_ = yield string("LETTERS ") >> text
    steps = yield block
    return Letters(text_, assign_to, steps)

