import pytest

from scriic.run import FileRunner
from scriic.errors import (
    ScriicSyntaxException,
    MissingMetadataException,
    InvalidMetadataException,
    NoReturnValueException
)


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
            FileRunner(tmp_file.absolute())

    def test_multi_howto(self, tmp_path):
        tmp_file = tmp_path / 'test.scriic'
        tmp_file.write_text("""
            HOWTO Make a <filling> sandwich on <surface>
            HOWTO Make a <filling> sandwich on <surface>
        """.strip())

        with pytest.raises(InvalidMetadataException):
            FileRunner(tmp_file.absolute())


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

    def test_title(self, tmp_path):
        tmp_file = tmp_path / 'test.scriic'
        tmp_file.write_text("""
            HOWTO Test <param>
        """.strip())

        runner = FileRunner(tmp_file.absolute())
        step = runner.run({'param': 'scriic'})

        assert step.text() == 'Test scriic'
        assert len(step.children) == 0

    def test_do(self, tmp_path):
        tmp_file = tmp_path / 'test.scriic'
        tmp_file.write_text("""
            HOWTO Test scriic
            DO Test scriic!
            DO Test scriic again!
        """.strip())

        runner = FileRunner(tmp_file.absolute())
        step = runner.run()

        assert step.children[0].text() == 'Test scriic!'
        assert step.children[1].text() == 'Test scriic again!'

    def test_do_substitution(self, tmp_path):
        tmp_file = tmp_path / 'test.scriic'
        tmp_file.write_text("""
            HOWTO Test <var>
            DO Test [var]!
        """.strip())

        runner = FileRunner(tmp_file.absolute())
        step = runner.run({'var': 'scriic'})

        assert step.children[0].text() == 'Test scriic!'

    def test_set(self, tmp_path):
        tmp_file = tmp_path / 'test.scriic'
        tmp_file.write_text("""
            HOWTO Test scriic
            SET var DOING Get some value
            DO Read [var]
        """.strip())

        runner = FileRunner(tmp_file.absolute())
        step = runner.run()

        assert len(step.children) == 2
        assert step.children[0].text() == 'Get some value'

        step.children[0].display_index = 1
        assert step.children[1].text() == 'Read the result of step 1'


class TestSub:
    def test_sub_simple(self, tmp_path):
        tmp_file_1 = tmp_path / 'test1.scriic'
        tmp_file_1.write_text("""
            HOWTO Test scriic
            DO This is in file 1
            SUB ./test2.scriic
        """.strip())

        tmp_file_2 = tmp_path / 'test2.scriic'
        tmp_file_2.write_text("""
            HOWTO Test subscriic
            DO This is in file 2
        """.strip())

        runner = FileRunner(tmp_file_1.absolute())
        step = runner.run()

        assert len(step.children) == 2
        assert step.children[0].text() == 'This is in file 1'
        assert step.children[1].text() == 'Test subscriic'
        assert len(step.children[1].children) == 1
        assert step.children[1].children[0].text() == 'This is in file 2'

    def test_sub_param(self, tmp_path):
        tmp_file_1 = tmp_path / 'test1.scriic'
        tmp_file_1.write_text("""
            HOWTO Test scriic with <param>
            DO This is in file 1

            SUB ./test2.scriic
            WITH [param] AS param
            GO
        """.strip())

        tmp_file_2 = tmp_path / 'test2.scriic'
        tmp_file_2.write_text("""
            HOWTO Test subscriic with <param>
            DO The value of param is [param]
        """.strip())

        runner = FileRunner(tmp_file_1.absolute())
        step = runner.run({'param': 'ABC'})

        assert len(step.children) == 2
        assert step.children[0].text() == 'This is in file 1'
        assert step.children[1].text() == 'Test subscriic with ABC'
        assert len(step.children[1].children) == 1
        assert step.children[1].children[0].text() == 'The value of param is ABC'

    def test_sub_return(self, tmp_path):
        tmp_file_1 = tmp_path / 'test1.scriic'
        tmp_file_1.write_text("""
            HOWTO Test scriic
            SUB ./test2.scriic INTO val
            DO Subscriic returned [val]
        """.strip())

        tmp_file_2 = tmp_path / 'test2.scriic'
        tmp_file_2.write_text("""
            HOWTO Test subscriic
            RETURN ABC
        """.strip())

        runner = FileRunner(tmp_file_1.absolute())
        step = runner.run()

        assert len(step.children) == 2
        assert step.children[0].text() == 'Test subscriic'
        assert len(step.children[0].children) == 0
        assert step.children[1].text() == 'Subscriic returned ABC'

    def test_sub_param_and_return(self, tmp_path):
        tmp_file_1 = tmp_path / 'test1.scriic'
        tmp_file_1.write_text("""
            HOWTO Test scriic
            SUB ./test2.scriic INTO val
            WITH ABC AS param
            GO
            DO Subscriic returned [val]
        """.strip())

        tmp_file_2 = tmp_path / 'test2.scriic'
        tmp_file_2.write_text("""
            HOWTO Test subscriic with <param>
            DO Received [param]
            RETURN DEF
        """.strip())

        runner = FileRunner(tmp_file_1.absolute())
        step = runner.run()

        assert len(step.children) == 2
        assert step.children[0].text() == 'Test subscriic with ABC'
        assert len(step.children[0].children) == 1
        assert step.children[0].children[0].text() == 'Received ABC'
        assert step.children[1].text() == 'Subscriic returned DEF'

    def test_sub_missing_return(self, tmp_path):
        tmp_file_1 = tmp_path / 'test1.scriic'
        tmp_file_1.write_text("""
            HOWTO Test scriic
            SUB ./test2.scriic INTO val
        """.strip())

        tmp_file_2 = tmp_path / 'test2.scriic'
        tmp_file_2.write_text("""
            HOWTO Test subscriic
            DO not return anything
        """.strip())

        runner = FileRunner(tmp_file_1.absolute())
        with pytest.raises(NoReturnValueException):
            runner.run()

    def test_unexpected_go(self, tmp_path):
        tmp_file = tmp_path / 'test.scriic'
        tmp_file.write_text("""
            HOWTO Test scriic
            GO
        """.strip())

        runner = FileRunner(tmp_file.absolute())
        with pytest.raises(ScriicSyntaxException):
            runner.run()

    def test_unfinished_sub(self, tmp_path):
        tmp_file_1 = tmp_path / 'test1.scriic'
        tmp_file_1.write_text("""
            HOWTO Test scriic
            SUB ./test2.scriic
        """.strip())

        tmp_file_2 = tmp_path / 'test2.scriic'
        tmp_file_2.write_text("""
            HOWTO Test subscriic with <param>
        """.strip())

        runner = FileRunner(tmp_file_1.absolute())
        with pytest.raises(ScriicSyntaxException):
            runner.run()

    def test_sub_nonexistant_file(self, tmp_path):
        tmp_file = tmp_path / 'test.scriic'
        tmp_file.write_text("""
            HOWTO Test scriic
            SUB ./nonexistant.sub
        """.strip())

        runner = FileRunner(tmp_file.absolute())
        with pytest.raises(FileNotFoundError):
            runner.run()
