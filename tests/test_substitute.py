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


def test_invalid_variable():
    with pytest.raises(ScriicRuntimeException):
        substitute_variables('[var]', {})
