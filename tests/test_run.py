import pytest

from scriic.errors import ScriicRuntimeException, ScriicSyntaxException
from scriic.run import FileRunner


def test_unknown_command(tmp_path):
    tmp_file = tmp_path / "test.scriic"
    tmp_file.write_text(
        """
        HOWTO Test scriic
        WHERE THERE ARE INVALID COMMANDS
        """
    )

    with pytest.raises(ScriicSyntaxException):
        FileRunner(tmp_file.absolute())


def test_title(tmp_path):
    tmp_file = tmp_path / "test.scriic"
    tmp_file.write_text(
        """
        HOWTO Test <param>
        """
    )

    runner = FileRunner(tmp_file.absolute())
    instruction = runner.run({"param": "scriic"})

    assert instruction.text() == "Test scriic"
    assert len(instruction.children) == 0


def test_missing_end(tmp_path):
    tmp_file = tmp_path / "test.scriic"
    tmp_file.write_text(
        """
        HOWTO Test scriic
        LETTERS char IN Hello
            DO [char]
        """
    )

    with pytest.raises(ScriicSyntaxException):
        FileRunner(tmp_file.absolute())
