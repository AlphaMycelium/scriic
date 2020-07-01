from parsy import *

from scriic.parser.do import do
from scriic.parser.howto import howto
from scriic.parser.letters import letters
from scriic.parser.primitives import newline
from scriic.parser.repeat import repeat
from scriic.parser.return_ import return_
from scriic.parser.sub import sub

step = do | sub | return_ | repeat | letters


@generate
def program():
    """An entire Scriic program."""
    yield whitespace.optional()
    title = yield howto
    steps = yield (newline >> step.sep_by(newline)) | success(list())
    yield whitespace.optional()
    return title, steps


def parse(text):
    """
    Parse some text as a Scriic program and return an AST.

    :param text: Program to parse.
    :raises ParseError: There is a syntax error in the program.
    """
    return program.parse(text)
