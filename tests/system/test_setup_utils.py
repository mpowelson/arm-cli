import pytest
from unittest import mock

from arm_cli.system.setup_utils import setup_xhost, is_line_in_file


@pytest.fixture
def temp_file(tmp_path):
    """Creates a temporary file for testing file operations."""
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("existing line\n")
    return test_file


def test_setup_xhost():
    """Test that setup_xhost runs the xhost command correctly."""
    with mock.patch("subprocess.run") as mock_run:
        setup_xhost()
        mock_run.assert_called_once_with(["xhost", "+local:docker"], check=True)


def test_is_line_in_file_exists(temp_file):
    """Test if the function correctly detects an existing line."""
    assert is_line_in_file("existing line", temp_file)


def test_is_line_in_file_not_exists(temp_file):
    """Test if the function correctly returns False for a missing line."""
    assert not is_line_in_file("missing line", temp_file)
