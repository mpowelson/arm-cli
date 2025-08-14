import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import click
import pytest
from click.testing import CliRunner

from arm_cli.config import Config, ProjectConfig
from arm_cli.projects.projects import projects


@pytest.fixture
def runner():
    """Fixture to provide a CliRunner instance."""
    return CliRunner()


@pytest.fixture
def temp_project_config():
    """Create a temporary project configuration."""
    config_data = {
        "name": "test-project",
        "description": "Test project for unit tests",
        "project_directory": "/tmp/test-project",
        "docker_compose_file": "docker-compose.yml",
        "data_directory": "/DATA",
    }
    return config_data


@pytest.fixture
def mock_config(temp_project_config):
    """Create a mock config with an active project."""
    config = Config(active_project="/tmp/test-project-config.json")
    return config


def test_projects_cd_no_active_project(runner):
    """Test that cd command fails when no active project is configured."""
    with patch("arm_cli.projects.projects.get_active_project_config") as mock_get_config:
        mock_get_config.return_value = None

        result = runner.invoke(projects, ["cd"], obj={"config": Config()})

        assert result.exit_code == 1
        assert "No active project configured" in result.output


def test_projects_cd_no_project_directory(runner, mock_config):
    """Test that cd command fails when project has no directory configured."""
    project_config = ProjectConfig(name="test", project_directory=None)

    with patch("arm_cli.projects.projects.get_active_project_config") as mock_get_config:
        mock_get_config.return_value = project_config

        result = runner.invoke(projects, ["cd"], obj={"config": mock_config})

        assert result.exit_code == 1
        assert "No project directory configured" in result.output


def test_projects_cd_directory_does_not_exist(runner, mock_config):
    """Test that cd command fails when project directory doesn't exist."""
    project_config = ProjectConfig(name="test", project_directory="/nonexistent/path")

    with patch("arm_cli.projects.projects.get_active_project_config") as mock_get_config:
        mock_get_config.return_value = project_config

        result = runner.invoke(projects, ["cd"], obj={"config": mock_config})

        assert result.exit_code == 1
        assert "Project directory does not exist" in result.output


def test_projects_cd_success(runner, mock_config):
    """Test that cd command succeeds with valid project directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_config = ProjectConfig(name="test", project_directory=temp_dir)

        with patch("arm_cli.projects.projects.get_active_project_config") as mock_get_config:
            mock_get_config.return_value = project_config

            result = runner.invoke(projects, ["cd"], obj={"config": mock_config})

            assert result.exit_code == 0
            assert "Changed to project directory" in result.output
            assert temp_dir in result.output


def test_projects_info_no_active_project(runner):
    """Test that info command handles no active project gracefully."""
    with patch("arm_cli.projects.projects.get_active_project_config") as mock_get_config:
        mock_get_config.return_value = None

        result = runner.invoke(projects, ["info"], obj={"config": Config()})

        assert result.exit_code == 0
        assert "No active project configured" in result.output


def test_projects_info_with_project(runner, mock_config, temp_project_config):
    """Test that info command displays project information correctly."""
    project_config = ProjectConfig(**temp_project_config)

    with patch("arm_cli.projects.projects.get_active_project_config") as mock_get_config:
        mock_get_config.return_value = project_config

        result = runner.invoke(projects, ["info"], obj={"config": mock_config})

        assert result.exit_code == 0
        assert "Active Project: test-project" in result.output
        assert "Description: Test project for unit tests" in result.output
        assert "Project Directory: /tmp/test-project" in result.output
        assert "Docker Compose File: docker-compose.yml" in result.output
        assert "Data Directory: /DATA" in result.output


def test_projects_info_minimal_project(runner, mock_config):
    """Test that info command works with minimal project configuration."""
    project_config = ProjectConfig(name="minimal-project")

    with patch("arm_cli.projects.projects.get_active_project_config") as mock_get_config:
        mock_get_config.return_value = project_config

        result = runner.invoke(projects, ["info"], obj={"config": mock_config})

        assert result.exit_code == 0
        assert "Active Project: minimal-project" in result.output


def test_projects_help(runner):
    """Test that projects command shows help."""
    result = runner.invoke(projects, ["--help"])

    assert result.exit_code == 0
    assert "Manage ARM projects" in result.output
    assert "cd" in result.output
    assert "info" in result.output
