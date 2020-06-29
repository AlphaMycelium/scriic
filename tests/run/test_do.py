from scriic.run import FileRunner


def test_do(tmp_path):
    tmp_file = tmp_path / "test.scriic"
    tmp_file.write_text(
        """
        HOWTO Test scriic
        DO Test scriic!
        DO Test scriic again!
        """
    )

    runner = FileRunner(tmp_file.absolute())
    instruction = runner.run()

    assert instruction.children[0].text() == "Test scriic!"
    assert instruction.children[1].text() == "Test scriic again!"


def test_do_substitution(tmp_path):
    tmp_file = tmp_path / "test.scriic"
    tmp_file.write_text(
        """
        HOWTO Test <var>
        DO Test [var]!
        """
    )

    runner = FileRunner(tmp_file.absolute())
    instruction = runner.run({"var": "scriic"})

    assert instruction.children[0].text() == "Test scriic!"


def test_do_with_variable(tmp_path):
    tmp_file = tmp_path / "test.scriic"
    tmp_file.write_text(
        """
        HOWTO Test scriic
        var = DO Get some value
        DO Read [var]
        """
    )

    runner = FileRunner(tmp_file.absolute())
    instruction = runner.run()

    assert len(instruction.children) == 2
    assert instruction.children[0].text() == "Get some value"

    instruction.children[0].display_index = 1
    assert instruction.children[1].text() == "Read the result of instruction 1"
