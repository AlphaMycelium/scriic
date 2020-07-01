from parsy import *

from scriic.parser.primitives import text

Return = namedtuple("Return", "value")


@generate("RETURN")
def return_():
    yield string("RETURN ")
    value = yield text
    return Return(value)
