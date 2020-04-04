from scriic.run import FileRunner


def test_repeat_known(tmp_path):
    tmp_file = tmp_path / 'test.scriic'
    tmp_file.write_text("""
        HOWTO Test scriic
        REPEAT 5
            DO Something
        END
    """.strip())

    runner = FileRunner(tmp_file.absolute())
    step = runner.run()

    assert len(step.children) == 5
    for child in step.children:
        assert child.text() == 'Something'


def test_repeat_unknown(tmp_path):
    tmp_file = tmp_path / 'test.scriic'
    tmp_file.write_text("""
        HOWTO Test scriic
        times = DO Get a number
        REPEAT times
            DO Something
        END
    """.strip())

    runner = FileRunner(tmp_file.absolute())
    step = runner.run()

    assert len(step.children) == 3
    assert step.children[0].text() == 'Get a number'
    step.children[0].display_index = 1
    assert step.children[1].text() == 'Something'
    step.children[1].display_index = 2
    assert step.children[2].text() == (
        'Go to step 2 and repeat the number of times from step 1')
