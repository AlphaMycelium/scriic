from parsy import *

from scriic.parser.primitives import assignment, text

Do = namedtuple("Do", "text assign_to")


@generate("DO")
def do():
    assign_to = yield assignment.optional()
    instruction = yield string("DO ") >> text
    return Do(instruction, assign_to)
