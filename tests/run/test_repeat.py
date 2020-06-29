from scriic.run import FileRunner


def test_repeat_known(tmp_path):
    tmp_file = tmp_path / "test.scriic"
    tmp_file.write_text(
        """
        HOWTO Test scriic
        REPEAT 5
            DO Something
        END
        """
    )

    runner = FileRunner(tmp_file.absolute())
    instruction = runner.run()

    assert len(instruction.children) == 5
    for child in instruction.children:
        assert child.text() == "Something"


def test_repeat_unknown(tmp_path):
    tmp_file = tmp_path / "test.scriic"
    tmp_file.write_text(
        """
        HOWTO Test scriic
        times = DO Get a number
        REPEAT times
            DO Something
        END
        """
    )

    runner = FileRunner(tmp_file.absolute())
    instruction = runner.run()

    assert len(instruction.children) == 3
    assert instruction.children[0].text() == "Get a number"
    instruction.children[0].display_index = 1
    assert instruction.children[1].text() == "Something"
    instruction.children[1].display_index = 2
    assert instruction.children[2].text() == (
        "Go to instruction 2 and repeat the number of times from instruction 1"
    )
