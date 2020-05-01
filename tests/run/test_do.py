from scriic.run import FileRunner


def test_do(tmp_path):
    tmp_file = tmp_path / "test.scriic"
    tmp_file.write_text(
        """
        HOWTO Test scriic
        DO Test scriic!
        DO Test scriic again!
    """.strip()
    )

    runner = FileRunner(tmp_file.absolute())
    step = runner.run()

    assert step.children[0].text() == "Test scriic!"
    assert step.children[1].text() == "Test scriic again!"


def test_do_substitution(tmp_path):
    tmp_file = tmp_path / "test.scriic"
    tmp_file.write_text(
        """
        HOWTO Test <var>
        DO Test [var]!
    """.strip()
    )

    runner = FileRunner(tmp_file.absolute())
    step = runner.run({"var": "scriic"})

    assert step.children[0].text() == "Test scriic!"


def test_do_with_variable(tmp_path):
    tmp_file = tmp_path / "test.scriic"
    tmp_file.write_text(
        """
        HOWTO Test scriic
        var = DO Get some value
        DO Read [var]
    """.strip()
    )

    runner = FileRunner(tmp_file.absolute())
    step = runner.run()

    assert len(step.children) == 2
    assert step.children[0].text() == "Get some value"

    step.children[0].display_index = 1
    assert step.children[1].text() == "Read the result of step 1"
