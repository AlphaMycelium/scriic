import pytest

from scriic.step import Step
from scriic.errors import UnsetDisplayIndexException


def test_step_text():
    step = Step('Hello ', 'world!')
    assert step.text() == 'Hello world!'


def test_step_leaves():
    step1 = Step()
    step2 = Step()
    step1.children.append(step2)
    step3 = Step()
    step2.children.append(step3)
    step4 = Step()
    step2.children.append(step4)

    leaves = list(step1.leaf_nodes())
    assert len(leaves) == 2
    assert leaves[0] == step3
    assert leaves[1] == step4


def test_repr():
    step = Step()
    step.display_index = 1
    assert str(step) == 'step 1'


def test_raises_unset_display_index():
    step = Step()
    with pytest.raises(UnsetDisplayIndexException):
        str(step)
