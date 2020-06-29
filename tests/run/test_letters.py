from scriic.run import FileRunner


def test_letters_known(tmp_path):
    tmp_file = tmp_path / "test.scriic"
    tmp_file.write_text(
        """
        HOWTO Test scriic
        char = LETTERS Hello
            DO [char]
        END
        """
    )

    runner = FileRunner(tmp_file.absolute())
    instruction = runner.run()

    assert len(instruction.children) == 5
    for i, char in enumerate("Hello"):
        assert instruction.children[i].text() == char


def test_letters_no_var(tmp_path):
    tmp_file = tmp_path / "test.scriic"
    tmp_file.write_text(
        """
        HOWTO Test scriic
        LETTERS Hello
            DO Something
        END
        """
    )

    runner = FileRunner(tmp_file.absolute())
    instruction = runner.run()

    assert len(instruction.children) == 5
    for i in range(5):
        assert instruction.children[i].text() == "Something"


def test_letters_unknown(tmp_path):
    tmp_file = tmp_path / "test.scriic"
    tmp_file.write_text(
        """
        HOWTO Test scriic
        string = DO Get a string
        char = LETTERS [string]
            DO Say [char"]
        END
        """
    )

    runner = FileRunner(tmp_file.absolute())
    instruction = runner.run()

    assert len(instruction.children) == 4
    assert instruction.children[0].text() == "Get a string"
    instruction.children[0].display_index = 1
    assert instruction.children[1].text() == (
        "Get the first letter of the result of instruction 1, or the next letter "
        "if you are returning from a future instruction"
    )
    instruction.children[1].display_index = 2
    assert instruction.children[2].text() == "Say the result of instruction 2"
    assert instruction.children[3].text() == (
        "If you haven't yet reached the last letter of the result of "
        "instruction 1, go to instruction 2"
    )
