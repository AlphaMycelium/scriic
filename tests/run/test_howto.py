import pytest

from scriic.errors import ScriicSyntaxException
from scriic.run import FileRunner


def test_howto(tmp_path):
    tmp_file = tmp_path / "test.scriic"
    tmp_file.write_text(
        """
        HOWTO Make a <filling> sandwich on <surface>
    """.strip()
    )

    runner = FileRunner(tmp_file.absolute())
    assert runner.title == "Make a <filling> sandwich on <surface>"
    assert runner.params == ["filling", "surface"]


def test_no_howto(tmp_path):
    tmp_file = tmp_path / "test.scriic"
    tmp_file.write_text(
        """
        DO Something
    """.strip()
    )

    with pytest.raises(ScriicSyntaxException):
        FileRunner(tmp_file.absolute())


def test_multi_howto(tmp_path):
    # This is discouraged from use however since it is mentioned as
    # possible in the docs we test that it behaves as described
    tmp_file = tmp_path / "test.scriic"
    tmp_file.write_text(
        """
        HOWTO Title 1
        HOWTO Title 2
    """.strip()
    )

    runner = FileRunner(tmp_file.absolute())
    assert runner.title == "Title 2"


def test_quoted_param(tmp_path):
    tmp_file = tmp_path / "test.scriic"
    tmp_file.write_text(
        """
        HOWTO Read <book_title">
    """.strip()
    )

    runner = FileRunner(tmp_file.absolute())
    assert runner.title == 'Read <book_title">'
    assert runner.params == ["book_title"]
