import pytest

from scriic.errors import ScriicRuntimeException, ScriicSyntaxException
from scriic.run import FileRunner


def test_sub(tmp_path):
    tmp_file_1 = tmp_path / "test1.scriic"
    tmp_file_1.write_text(
        """
        HOWTO Test scriic
        DO This is in file 1
        SUB ./test2.scriic
        """
    )

    tmp_file_2 = tmp_path / "test2.scriic"
    tmp_file_2.write_text(
        """
        HOWTO Test subscriic
        DO This is in file 2
        """
    )

    runner = FileRunner(tmp_file_1.absolute())
    instruction = runner.run()

    assert len(instruction.children) == 2
    assert instruction.children[0].text() == "This is in file 1"
    assert instruction.children[1].text() == "Test subscriic"
    assert len(instruction.children[1].children) == 1
    assert instruction.children[1].children[0].text() == "This is in file 2"


def test_sub_param(tmp_path):
    tmp_file_1 = tmp_path / "test1.scriic"
    tmp_file_1.write_text(
        """
        HOWTO Test scriic with <param>
        DO This is in file 1

        SUB ./test2.scriic
        PRM param = [param]
        GO
        """
    )

    tmp_file_2 = tmp_path / "test2.scriic"
    tmp_file_2.write_text(
        """
        HOWTO Test subscriic with <param>
        DO The value of param is [param]
        """
    )

    runner = FileRunner(tmp_file_1.absolute())
    instruction = runner.run({"param": "ABC"})

    assert len(instruction.children) == 2
    assert instruction.children[0].text() == "This is in file 1"
    assert instruction.children[1].text() == "Test subscriic with ABC"
    assert len(instruction.children[1].children) == 1
    assert instruction.children[1].children[0].text() == "The value of param is ABC"


def test_sub_return(tmp_path):
    tmp_file_1 = tmp_path / "test1.scriic"
    tmp_file_1.write_text(
        """
        HOWTO Test scriic
        val = SUB ./test2.scriic
        DO Subscriic returned [val]
        """
    )

    tmp_file_2 = tmp_path / "test2.scriic"
    tmp_file_2.write_text(
        """
        HOWTO Test subscriic
        RETURN ABC
        """
    )

    runner = FileRunner(tmp_file_1.absolute())
    instruction = runner.run()

    assert len(instruction.children) == 2
    assert instruction.children[0].text() == "Test subscriic"
    assert len(instruction.children[0].children) == 0
    assert instruction.children[1].text() == "Subscriic returned ABC"


def test_sub_param_and_return(tmp_path):
    tmp_file_1 = tmp_path / "test1.scriic"
    tmp_file_1.write_text(
        """
        HOWTO Test scriic
        val = SUB ./test2.scriic
        PRM param = ABC
        GO
        DO Subscriic returned [val]
        """
    )

    tmp_file_2 = tmp_path / "test2.scriic"
    tmp_file_2.write_text(
        """
        HOWTO Test subscriic with <param>
        DO Received [param]
        RETURN DEF
        """
    )

    runner = FileRunner(tmp_file_1.absolute())
    instruction = runner.run()

    assert len(instruction.children) == 2
    assert instruction.children[0].text() == "Test subscriic with ABC"
    assert len(instruction.children[0].children) == 1
    assert instruction.children[0].children[0].text() == "Received ABC"
    assert instruction.children[1].text() == "Subscriic returned DEF"


def test_sub_missing_return(tmp_path):
    tmp_file_1 = tmp_path / "test1.scriic"
    tmp_file_1.write_text(
        """
        HOWTO Test scriic
        val = SUB ./test2.scriic
        """
    )

    tmp_file_2 = tmp_path / "test2.scriic"
    tmp_file_2.write_text(
        """
        HOWTO Test subscriic
        DO not return anything
        """
    )

    runner = FileRunner(tmp_file_1.absolute())
    with pytest.raises(ScriicRuntimeException):
        runner.run()


def test_unexpected_go(tmp_path):
    tmp_file = tmp_path / "test.scriic"
    tmp_file.write_text(
        """
        HOWTO Test scriic
        GO
        """
    )

    with pytest.raises(ScriicSyntaxException):
        runner = FileRunner(tmp_file.absolute())


def test_unexpected_sub(tmp_path):
    tmp_file_1 = tmp_path / "test1.scriic"
    tmp_file_1.write_text(
        """
        HOWTO Test scriic
        SUB ./test2.scriic
        PRM param = ABC
        SUB ./test3.scriic
        GO
        """
    )

    tmp_file_2 = tmp_path / "test2.scriic"
    tmp_file_2.write_text(
        """
        HOWTO Test scriic 2 with <param>
        """
    )

    tmp_file_3 = tmp_path / "test3.scriic"
    tmp_file_3.write_text(
        """
        HOWTO Test scriic 3
        """
    )

    with pytest.raises(ScriicSyntaxException):
        runner = FileRunner(tmp_file_1.absolute())


def test_unfinished_sub(tmp_path):
    tmp_file_1 = tmp_path / "test1.scriic"
    tmp_file_1.write_text(
        """
        HOWTO Test scriic
        SUB ./test2.scriic
        """
    )

    tmp_file_2 = tmp_path / "test2.scriic"
    tmp_file_2.write_text(
        """
        HOWTO Test subscriic with <param>
        """
    )

    runner = FileRunner(tmp_file_1.absolute())
    with pytest.raises(ScriicRuntimeException):
        runner.run()


def test_sub_nonexistant_file(tmp_path):
    tmp_file = tmp_path / "test.scriic"
    tmp_file.write_text(
        """
        HOWTO Test scriic
        SUB ./nonexistant.sub
        """
    )

    runner = FileRunner(tmp_file.absolute())
    with pytest.raises(FileNotFoundError):
        runner.run()
