import pytest

from scriic.substitute import substitute_variables
from scriic.errors import ScriicRuntimeException


def test_substitution():
    assert substitute_variables('[var]', {'var': 'X'}) == ['X']
    assert substitute_variables('XXX[var]XXX', {'var': 'Y'}) == ['XXX', 'Y', 'XXX']


def test_no_substitution():
    assert substitute_variables('var', {'var': 'X'}) == ['var']
    assert substitute_variables('[var', {'var': 'X'}) == ['[var']
    assert substitute_variables('var]', {'var': 'X'}) == ['var]']


def test_quotation_marks():
    assert substitute_variables('[x"]', {'x': 'X'}) == ['"', 'X', '"']
    assert substitute_variables('<x">', {'x': 'X'}, True) == ['"', 'X', '"']


def test_no_quotation_marks_on_unknown():
    from scriic.unknown import UnknownValue
    from scriic.step import Step

    step = Step()
    step.display_index = 1
    unknown = UnknownValue(step)

    assert substitute_variables('[x"]', {'x': unknown}) == [unknown]
    assert substitute_variables('<x">', {'x': unknown}, True) == [unknown]


def test_invalid_variable():
    with pytest.raises(ScriicRuntimeException):
        substitute_variables('[var]', {})
