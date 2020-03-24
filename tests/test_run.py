import pytest

from scriic.run import *


class TestMetadata:
    def test_howto(self, tmp_path):
        tmp_file = tmp_path / 'test.scriic'
        tmp_file.write_text("""
            HOWTO Make a <filling> sandwich on <surface>
        """.strip())

        runner = FileRunner(tmp_file.absolute())
        assert runner.title == 'Make a <filling> sandwich on <surface>'
        assert runner.code_begins_at == 1

    def test_no_howto(self, tmp_path):
        tmp_file = tmp_path / 'test.scriic'
        tmp_file.write_text("""
            DO Something
        """.strip())

        with pytest.raises(MissingMetadataException):
            runner = FileRunner(tmp_file.absolute())

    def test_multi_howto(self, tmp_path):
        tmp_file = tmp_path / 'test.scriic'
        tmp_file.write_text("""
            HOWTO Make a <filling> sandwich on <surface>
            HOWTO Make a <filling> sandwich on <surface>
        """.strip())

        with pytest.raises(InvalidMetadataException):
            runner = FileRunner(tmp_file.absolute())


class TestRun:
    def test_invalid_syntax(self, tmp_path):
        tmp_file = tmp_path / 'test.scriic'
        tmp_file.write_text("""
            HOWTO Test scriic
            WHERE THERE ARE INVALID COMMANDS
        """.strip())

        runner = FileRunner(tmp_file.absolute())
        with pytest.raises(ScriicSyntaxException):
            runner.run()

    def test_do(self, tmp_path):
        tmp_file = tmp_path / 'test.scriic'
        tmp_file.write_text("""
            HOWTO Test scriic
            DO Test scriic!
            DO Test scriic again!
        """.strip())

        runner = FileRunner(tmp_file.absolute())
        steps = runner.run()

        assert len(steps) == 2
        assert steps[0] == 'Test scriic!'
        assert steps[1] == 'Test scriic again!'

    def test_do_substitution(self, tmp_path):
        tmp_file = tmp_path / 'test.scriic'
        tmp_file.write_text("""
            HOWTO Test <var>
            DO Test [var]!
        """.strip())

        runner = FileRunner(tmp_file.absolute())
        steps = runner.run({'var': 'scriic'})

        assert steps[0] == 'Test scriic!'

    def test_set(self, tmp_path):
        tmp_file = tmp_path / 'test.scriic'
        tmp_file.write_text("""
            HOWTO Test scriic
            SET var DOING Get some value
            DO Read [var]
        """.strip())

        runner = FileRunner(tmp_file.absolute())
        steps = runner.run()

        assert len(steps) == 2
        assert steps[0] == 'Get some value'
        assert steps[1] == 'Read the result of step 1'
