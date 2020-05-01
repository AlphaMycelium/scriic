from pathlib import Path

import pytest

from scriic.errors import ScriicSyntaxException
from scriic.run import FileRunner

# List all Scriicsics files
scriicsics_dir = Path(__file__).parent.parent / "scriicsics"
scriicsics = scriicsics_dir.glob("**/*.scriic")


@pytest.mark.parametrize("file_path", scriicsics)
def test_scriicsics_are_vaild(file_path):
    """Each Scriicsics file should parse without errors."""

    try:
        # This will attempt to parse the file
        FileRunner(file_path.absolute())
    except ScriicSyntaxException as e:
        # Create a more useful failure message
        relative_path = file_path.relative_to(scriicsics_dir)
        pytest.fail(f"{relative_path} raised a syntax exception: {e}")
