from parsy import *

from scriic.parser.primitives import variable

Parameter = namedtuple("Parameter", "name quoted")


@generate("parameter")
def parameter():
    """A <parameter> in a HOWTO line."""
    param = yield string("<") >> variable
    quoted = yield string('"').optional() << string(">")
    return Parameter(param, bool(quoted))


@generate("HOWTO")
def howto():
    yield string("HOWTO ")
    title = yield (parameter | regex(r"[^<\n]+")).at_least(1)
    return title
