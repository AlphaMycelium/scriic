from parsy import *


# Also captures indentation and trailing spaces
newline = regex(r'\s*\n\s*').desc("newline")

number = regex(r"\d+").map(int).desc("number")

variable = regex(r'[a-zA-Z_]\w*').desc("variable name")
assignment = variable << string(" = ").desc("variable assignment")


Substitution = namedtuple("Substitution", "name quoted")
@generate("substitution")
def substitution():
    """A [variable_substitution] in some text."""
    param = yield string("[") >> variable
    quoted = yield string('"').optional() << string("]")
    return Substitution(param, bool(quoted))

# A list of strings and variable substitutions to be concatenated together later
text = (substitution | regex(r"[^\[\n]+")).at_least(1)


@generate
def block():
    # This must be imported here to avoid circular imports
    from scriic.parser import step

    yield newline
    contents = yield step.sep_by(newline, min=1)
    yield newline >> string("END")
    return contents
