import pytest

from scriic.errors import UnsetDisplayIndexException
from scriic.step import Step


def test_step_leaves():
    step1 = Step("1")
    step2 = Step("2")
    step1.children.append(step2)
    step3 = Step("3")
    step2.children.append(step3)
    step4 = Step("4")
    step2.children.append(step4)

    leaves = list(step1.leaf_nodes())
    assert len(leaves) == 2
    assert leaves[0] == step3
    assert leaves[1] == step4


def test_repr():
    step = Step("1")
    step.display_index = 1
    assert str(step) == "step 1"


def test_raises_unset_display_index():
    step = Step("I don't have a display index")
    with pytest.raises(UnsetDisplayIndexException):
        str(step)
