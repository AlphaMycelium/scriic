import pytest

from scriic.errors import ScriicRuntimeException
from scriic.parser.howto import Parameter
from scriic.parser.primitives import Substitution
from scriic.substitute import substitute_variables


@pytest.mark.parametrize("s_type", [Substitution, Parameter])
def test_substitution(s_type):
    assert substitute_variables(["A", s_type("var", False), "C"], {"var": "B"}) == [
        "A",
        "B",
        "C",
    ]


@pytest.mark.parametrize("s_type", [Substitution, Parameter])
def test_quotation_marks(s_type):
    assert substitute_variables([s_type("x", True)], {"x": "X"}) == ['"', "X", '"']


@pytest.mark.parametrize("s_type", [Substitution, Parameter])
def test_no_quotation_marks_on_unknown(s_type):
    from scriic.value import UnknownValue
    from scriic.instruction import Instruction

    instruction = Instruction("text")
    instruction.display_index = 1
    unknown = UnknownValue(instruction)

    assert substitute_variables([s_type("x", True)], {"x": unknown}) == [unknown]


@pytest.mark.parametrize("s_type", [Substitution, Parameter])
def test_invalid_variable(s_type):
    with pytest.raises(ScriicRuntimeException):
        substitute_variables([s_type("var", False)], {})
