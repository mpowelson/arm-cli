import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from arm_cli.config import (
    EnvironmentConfig,
    GlobalContext,
    get_config_dir,
    get_config_file,
    load_config,
    load_project_config,
    save_config,
)


class TestGlobalContext:
    def test_global_context_default_values(self):
        """Test that GlobalContext has correct default values."""
        config = GlobalContext()
        assert config.active_project == ""

    def test_global_context_with_values(self):
        """Test that GlobalContext can be created with custom values."""
        config = GlobalContext(active_project="test-project")
        assert config.active_project == "test-project"

    def test_global_context_model_dump(self):
        """Test that GlobalContext can be serialized to dict."""
        config = GlobalContext(active_project="test-project")
        data = config.model_dump()
        assert data == {"active_project": "test-project", "available_projects": []}


class TestConfigFunctions:
    def test_get_config_dir(self):
        """Test that config directory is created correctly."""
        with patch("arm_cli.config.appdirs.user_config_dir") as mock_user_config_dir:
            mock_user_config_dir.return_value = "/tmp/test_config"

            config_dir = get_config_dir()

            assert config_dir == Path("/tmp/test_config")
            mock_user_config_dir.assert_called_once_with("arm-cli")

    def test_get_config_file(self):
        """Test that config file path is correct."""
        with patch("arm_cli.config.get_config_dir") as mock_get_config_dir:
            mock_get_config_dir.return_value = Path("/tmp/test_config")

            config_file = get_config_file()

            assert config_file == Path("/tmp/test_config/global_context.json")

    def test_save_config(self):
        """Test that config can be saved to file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("arm_cli.config.get_config_file") as mock_get_config_file:
                config_file = Path(temp_dir) / "config.json"
                mock_get_config_file.return_value = config_file

                config = GlobalContext(active_project="test-project")
                save_config(config)

                assert config_file.exists()
                with open(config_file, "r") as f:
                    data = json.load(f)

                assert data == {"active_project": "test-project", "available_projects": []}

    def test_load_config_new_file(self):
        """Test that new config file is created when it doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("arm_cli.config.get_config_file") as mock_get_config_file:
                config_file = Path(temp_dir) / "config.json"
                mock_get_config_file.return_value = config_file

                # File doesn't exist initially
                assert not config_file.exists()

                config = load_config()

                # File should be created with default values
                assert config_file.exists()
                assert config.active_project == ""

                # Verify file contents
                with open(config_file, "r") as f:
                    data = json.load(f)
                assert data == {"active_project": "", "available_projects": []}

    def test_load_config_existing_file(self):
        """Test that existing config file is loaded correctly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("arm_cli.config.get_config_file") as mock_get_config_file:
                config_file = Path(temp_dir) / "config.json"
                mock_get_config_file.return_value = config_file

                # Create existing config file
                existing_data = {"active_project": "existing-project"}
                with open(config_file, "w") as f:
                    json.dump(existing_data, f)

                config = load_config()

                assert config.active_project == "existing-project"

    def test_load_config_corrupted_file(self):
        """Test that corrupted config file is handled gracefully."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("arm_cli.config.get_config_file") as mock_get_config_file:
                config_file = Path(temp_dir) / "config.json"
                mock_get_config_file.return_value = config_file

                # Create corrupted config file
                with open(config_file, "w") as f:
                    f.write("invalid json content")

                config = load_config()

                # Should create new default config
                assert config.active_project == ""

                # Verify file was overwritten with valid JSON
                with open(config_file, "r") as f:
                    data = json.load(f)
                assert data == {"active_project": "", "available_projects": []}

    def test_load_config_missing_fields(self):
        """Test that config with missing fields is handled gracefully."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("arm_cli.config.get_config_file") as mock_get_config_file:
                config_file = Path(temp_dir) / "config.json"
                mock_get_config_file.return_value = config_file

                # Create config file with missing fields
                with open(config_file, "w") as f:
                    json.dump({}, f)

                config = load_config()

                # Should use default values for missing fields
                assert config.active_project == ""


class TestEnvironmentConfig:
    def test_project_config_default_values(self):
        """Test that EnvironmentConfig has correct default values."""
        config = EnvironmentConfig(name="test-project")
        assert config.name == "test-project"
        assert config.description is None
        assert config.project_directory is None

    def test_project_config_with_values(self):
        """Test that EnvironmentConfig can be created with custom values."""
        config = EnvironmentConfig(
            name="test-project",
            description="Test project",
            project_directory="/tmp/project",
        )
        assert config.name == "test-project"
        assert config.description == "Test project"
        assert config.project_directory == "/tmp/project"

    def test_project_config_model_dump(self):
        """Test that EnvironmentConfig can be serialized to dict."""
        config = EnvironmentConfig(
            name="test-project", description="Test project", project_directory="/tmp/project"
        )
        data = config.model_dump()
        expected = {
            "name": "test-project",
            "description": "Test project",
            "project_directory": "/tmp/project",
        }
        assert data == expected

    def test_get_resolved_project_directory_absolute(self):
        """Test that absolute project_directory paths are returned as-is."""
        config = EnvironmentConfig(name="test-project", project_directory="/absolute/path")
        resolved = config.get_resolved_project_directory(Path("/dummy/config.json"))
        assert resolved == "/absolute/path"

    def test_get_resolved_project_directory_relative(self):
        """Test that relative project_directory paths are resolved correctly."""
        config = EnvironmentConfig(name="test-project", project_directory="relative/path")
        config_file_path = Path("/config/location/config.json")
        resolved = config.get_resolved_project_directory(config_file_path)
        assert resolved == str(Path("/config/location/relative/path").resolve())

    def test_get_resolved_project_directory_none(self):
        """Test that None project_directory returns None."""
        config = EnvironmentConfig(name="test-project")
        resolved = config.get_resolved_project_directory(Path("/dummy/config.json"))
        assert resolved is None

    def test_get_resolved_project_directory_no_config_path(self):
        """Test that relative paths raise an error when no config path provided."""
        config = EnvironmentConfig(name="test-project", project_directory="relative/path")
        with pytest.raises(ValueError, match="config_file_path must be provided"):
            config.get_resolved_project_directory()

    def test_get_resolved_project_directory_tilde(self):
        """Test that tilde (~) is expanded to home directory."""
        config = EnvironmentConfig(name="test-project", project_directory="~/projects")
        resolved = config.get_resolved_project_directory(Path("/dummy/config.json"))
        assert resolved == str(Path.home() / "projects")
