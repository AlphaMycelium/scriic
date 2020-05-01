import pytest

from scriic.errors import ScriicRuntimeException
from scriic.substitute import substitute_variables


def test_substitution():
    assert substitute_variables("[var]", {"var": "X"}) == ["X"]
    assert substitute_variables("XXX[var]XXX", {"var": "Y"}) == ["XXX", "Y", "XXX"]


def test_no_substitution():
    assert substitute_variables("var", {"var": "X"}) == ["var"]
    assert substitute_variables("[var", {"var": "X"}) == ["[var"]
    assert substitute_variables("var]", {"var": "X"}) == ["var]"]


def test_quotation_marks():
    assert substitute_variables('[x"]', {"x": "X"}) == ['"', "X", '"']
    assert substitute_variables('<x">', {"x": "X"}, True) == ['"', "X", '"']


def test_no_quotation_marks_on_unknown():
    from scriic.value import UnknownValue
    from scriic.step import Step

    step = Step("text")
    step.display_index = 1
    unknown = UnknownValue(step)

    assert substitute_variables('[x"]', {"x": unknown}) == [unknown]
    assert substitute_variables('<x">', {"x": unknown}, True) == [unknown]


def test_invalid_variable():
    with pytest.raises(ScriicRuntimeException):
        substitute_variables("[var]", {})
