import pytest

from scriic.errors import ScriicSyntaxException
from scriic.parser.howto import Parameter
from scriic.run import FileRunner


def test_howto(tmp_path):
    tmp_file = tmp_path / "test.scriic"
    tmp_file.write_text(
        """
        HOWTO Make a <filling> sandwich on <surface>
        """
    )

    runner = FileRunner(tmp_file.absolute())
    assert runner.title == [
        "Make a ",
        Parameter("filling", False),
        " sandwich on ",
        Parameter("surface", False),
    ]
    assert runner.required_parameters == {"filling", "surface"}


def test_no_howto(tmp_path):
    tmp_file = tmp_path / "test.scriic"
    tmp_file.write_text(
        """
        DO Something
        """
    )

    with pytest.raises(ScriicSyntaxException):
        FileRunner(tmp_file.absolute())


def test_quoted_param(tmp_path):
    tmp_file = tmp_path / "test.scriic"
    tmp_file.write_text(
        """
        HOWTO Read <book_title">
        """
    )

    runner = FileRunner(tmp_file.absolute())
    assert runner.title == ["Read ", Parameter("book_title", True)]
    assert runner.required_parameters == {"book_title"}
