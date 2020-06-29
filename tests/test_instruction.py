import pytest

from scriic.errors import UnsetDisplayIndexException
from scriic.instruction import Instruction


def test_instruction_leaves():
    instruction1 = Instruction("1")
    instruction2 = Instruction("2")
    instruction1.children.append(instruction2)
    instruction3 = Instruction("3")
    instruction2.children.append(instruction3)
    instruction4 = Instruction("4")
    instruction2.children.append(instruction4)

    leaves = list(instruction1.leaf_nodes())
    assert len(leaves) == 2
    assert leaves[0] == instruction3
    assert leaves[1] == instruction4


def test_repr():
    instruction = Instruction("1")
    instruction.display_index = 1
    assert str(instruction) == "instruction 1"


def test_raises_unset_display_index():
    instruction = Instruction("I don't have a display index")
    with pytest.raises(UnsetDisplayIndexException):
        str(instruction)
