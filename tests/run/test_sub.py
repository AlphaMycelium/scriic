import pytest

from scriic.errors import ScriicRuntimeException
from scriic.run import FileRunner


def test_sub(tmp_path):
    tmp_file_1 = tmp_path / "test1.scriic"
    tmp_file_1.write_text(
        """
        HOWTO Test scriic
        DO This is in file 1
        SUB ./test2.scriic
    """.strip()
    )

    tmp_file_2 = tmp_path / "test2.scriic"
    tmp_file_2.write_text(
        """
        HOWTO Test subscriic
        DO This is in file 2
    """.strip()
    )

    runner = FileRunner(tmp_file_1.absolute())
    step = runner.run()

    assert len(step.children) == 2
    assert step.children[0].text() == "This is in file 1"
    assert step.children[1].text() == "Test subscriic"
    assert len(step.children[1].children) == 1
    assert step.children[1].children[0].text() == "This is in file 2"


def test_sub_param(tmp_path):
    tmp_file_1 = tmp_path / "test1.scriic"
    tmp_file_1.write_text(
        """
        HOWTO Test scriic with <param>
        DO This is in file 1

        SUB ./test2.scriic
        PRM param = [param]
        GO
    """.strip()
    )

    tmp_file_2 = tmp_path / "test2.scriic"
    tmp_file_2.write_text(
        """
        HOWTO Test subscriic with <param>
        DO The value of param is [param]
    """.strip()
    )

    runner = FileRunner(tmp_file_1.absolute())
    step = runner.run({"param": "ABC"})

    assert len(step.children) == 2
    assert step.children[0].text() == "This is in file 1"
    assert step.children[1].text() == "Test subscriic with ABC"
    assert len(step.children[1].children) == 1
    assert step.children[1].children[0].text() == "The value of param is ABC"


def test_sub_return(tmp_path):
    tmp_file_1 = tmp_path / "test1.scriic"
    tmp_file_1.write_text(
        """
        HOWTO Test scriic
        val = SUB ./test2.scriic
        DO Subscriic returned [val]
    """.strip()
    )

    tmp_file_2 = tmp_path / "test2.scriic"
    tmp_file_2.write_text(
        """
        HOWTO Test subscriic
        RETURN ABC
    """.strip()
    )

    runner = FileRunner(tmp_file_1.absolute())
    step = runner.run()

    assert len(step.children) == 2
    assert step.children[0].text() == "Test subscriic"
    assert len(step.children[0].children) == 0
    assert step.children[1].text() == "Subscriic returned ABC"


def test_sub_param_and_return(tmp_path):
    tmp_file_1 = tmp_path / "test1.scriic"
    tmp_file_1.write_text(
        """
        HOWTO Test scriic
        val = SUB ./test2.scriic
        PRM param = ABC
        GO
        DO Subscriic returned [val]
    """.strip()
    )

    tmp_file_2 = tmp_path / "test2.scriic"
    tmp_file_2.write_text(
        """
        HOWTO Test subscriic with <param>
        DO Received [param]
        RETURN DEF
    """.strip()
    )

    runner = FileRunner(tmp_file_1.absolute())
    step = runner.run()

    assert len(step.children) == 2
    assert step.children[0].text() == "Test subscriic with ABC"
    assert len(step.children[0].children) == 1
    assert step.children[0].children[0].text() == "Received ABC"
    assert step.children[1].text() == "Subscriic returned DEF"


def test_sub_missing_return(tmp_path):
    tmp_file_1 = tmp_path / "test1.scriic"
    tmp_file_1.write_text(
        """
        HOWTO Test scriic
        val = SUB ./test2.scriic
    """.strip()
    )

    tmp_file_2 = tmp_path / "test2.scriic"
    tmp_file_2.write_text(
        """
        HOWTO Test subscriic
        DO not return anything
    """.strip()
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
    """.strip()
    )

    runner = FileRunner(tmp_file.absolute())
    with pytest.raises(ScriicRuntimeException):
        runner.run()


def test_unexpected_sub(tmp_path):
    tmp_file_1 = tmp_path / "test1.scriic"
    tmp_file_1.write_text(
        """
        HOWTO Test scriic
        SUB ./test2.scriic
        PRM param = ABC
        SUB ./test3.scriic
        GO
    """.strip()
    )

    tmp_file_2 = tmp_path / "test2.scriic"
    tmp_file_2.write_text(
        """
        HOWTO Test scriic 2 with <param>
    """.strip()
    )

    tmp_file_3 = tmp_path / "test3.scriic"
    tmp_file_3.write_text(
        """
        HOWTO Test scriic 3
    """.strip()
    )

    runner = FileRunner(tmp_file_1.absolute())
    with pytest.raises(ScriicRuntimeException):
        runner.run()


def test_unfinished_sub(tmp_path):
    tmp_file_1 = tmp_path / "test1.scriic"
    tmp_file_1.write_text(
        """
        HOWTO Test scriic
        SUB ./test2.scriic
    """.strip()
    )

    tmp_file_2 = tmp_path / "test2.scriic"
    tmp_file_2.write_text(
        """
        HOWTO Test subscriic with <param>
    """.strip()
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
    """.strip()
    )

    runner = FileRunner(tmp_file.absolute())
    with pytest.raises(FileNotFoundError):
        runner.run()
