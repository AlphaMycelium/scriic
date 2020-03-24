import pytest

from scriic.run import *


class TestMetadata:
    def test_metadata(self, tmp_path):
        tmp_file = tmp_path / 'test.scriic'
        tmp_file.write_text("""
            HOWTO Make a <filling> sandwich on <surface>
            WHERE filling IS opt
                Cheese
                Ham
                Tuna
            END
            WHERE surface IS str
        """.strip())

        runner = FileRunner(tmp_file.absolute())
        assert runner.howto == 'Make a <filling> sandwich on <surface>'
        assert runner.params['filling'] == ['Cheese', 'Ham', 'Tuna']
        assert runner.params['surface'] == 'str'
        assert runner.code_begins_at == 7

    def test_no_howto(self, tmp_path):
        tmp_file = tmp_path / 'test.scriic'
        tmp_file.write_text("""
            WHERE surface IS str
        """.strip())

        with pytest.raises(MetadataException):
            runner = FileRunner(tmp_file.absolute())

    def test_multi_howto(self, tmp_path):
        tmp_file = tmp_path / 'test.scriic'
        tmp_file.write_text("""
            HOWTO Make a <filling> sandwich on <surface>
            HOWTO Make a <filling> sandwich on <surface>
        """.strip())

        with pytest.raises(MetadataException):
            runner = FileRunner(tmp_file.absolute())

    @pytest.mark.parametrize('type', SUPPORTED_TYPES)
    def test_where_type(self, tmp_path, type):
        tmp_file = tmp_path / 'test.scriic'
        tmp_file.write_text(f"""
            HOWTO Make a <filling> sandwich
            WHERE filling IS {type}
        """.strip())

        runner = FileRunner(tmp_file.absolute())
        assert runner.params['filling'] == type

    def test_invalid_where_type(self, tmp_path):
        tmp_file = tmp_path / 'test.scriic'
        tmp_file.write_text("""
            HOWTO Make a <filling> sandwich
            WHERE filling IS list
        """.strip())

        with pytest.raises(MetadataException):
            runner = FileRunner(tmp_file.absolute())

    def test_invalid_where_param(self, tmp_path):
        tmp_file = tmp_path / 'test.scriic'
        tmp_file.write_text("""
            HOWTO Make a <filling> sandwich
            WHERE invalid IS str
        """.strip())

        with pytest.raises(MetadataException):
            runner = FileRunner(tmp_file.absolute())

    def test_missing_where_param(self, tmp_path):
        tmp_file = tmp_path / 'test.scriic'
        tmp_file.write_text("""
            HOWTO Make a <filling> sandwich
        """.strip())

        with pytest.raises(MetadataException):
            runner = FileRunner(tmp_file.absolute())

    def test_invalid_syntax(self, tmp_path):
        tmp_file = tmp_path / 'test.scriic'
        tmp_file.write_text("""
            HOWTO Make a <filling> sandwich
            WHERE filling HAS invalid syntax
        """.strip())

        with pytest.raises(ScriicSyntaxException):
            runner = FileRunner(tmp_file.absolute())


class TestRun:
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
            WHERE var IS str
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
