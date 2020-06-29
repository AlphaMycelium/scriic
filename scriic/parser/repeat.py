from parsy import *

from scriic.parser.primitives import variable, number, block


Repeat = namedtuple("Repeat", "times steps")


@generate("REPEAT")
def repeat():
    times = yield string("REPEAT ") >> (variable | number)
    steps = yield block
    return Repeat(times, steps)

