import pytest

from scriic.errors import ScriicRuntimeException, ScriicSyntaxException
from scriic.run import FileRunner


def test_unknown_command(tmp_path):
    tmp_file = tmp_path / "test.scriic"
    tmp_file.write_text(
        """
        HOWTO Test scriic
        WHERE THERE ARE INVALID COMMANDS
    """.strip()
    )

    with pytest.raises(ScriicSyntaxException):
        FileRunner(tmp_file.absolute())


def test_title(tmp_path):
    tmp_file = tmp_path / "test.scriic"
    tmp_file.write_text(
        """
        HOWTO Test <param>
    """.strip()
    )

    runner = FileRunner(tmp_file.absolute())
    step = runner.run({"param": "scriic"})

    assert step.text() == "Test scriic"
    assert len(step.children) == 0


def test_missing_end(tmp_path):
    tmp_file = tmp_path / "test.scriic"
    tmp_file.write_text(
        """
        HOWTO Test scriic
        LETTERS char IN Hello
            DO [char]
    """.strip()
    )

    runner = FileRunner(tmp_file.absolute())
    with pytest.raises(ScriicRuntimeException):
        runner.run()
