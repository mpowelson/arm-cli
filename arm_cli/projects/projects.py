import os
import subprocess
import sys
from pathlib import Path

import click

from arm_cli.config import get_active_project_config


@click.group()
def projects():
    """Manage ARM projects"""
    pass


@projects.command()
@click.pass_context
def cd(ctx):
    """Change to the active project directory"""
    config = ctx.obj["config"]

    # Get the active project configuration
    project_config = get_active_project_config(config)
    if not project_config:
        print(
            "No active project configured. Use 'arm-cli self config --project <path>' to set one."
        )
        sys.exit(1)

    # Get the project directory
    project_dir = project_config.project_directory
    if not project_dir:
        print("No project directory configured in the active project.")
        sys.exit(1)

    # Expand the path (handle ~ for home directory)
    project_path = Path(project_dir).expanduser().resolve()

    if not project_path.exists():
        print(f"Project directory does not exist: {project_path}")
        sys.exit(1)

    if not project_path.is_dir():
        print(f"Project directory is not a directory: {project_path}")
        sys.exit(1)

    # Change to the project directory
    try:
        os.chdir(project_path)
        print(f"Changed to project directory: {project_path}")

        # If we're in a shell, we can't actually change the parent process directory
        # So we'll print the command that the user should run
        if os.getenv("SHELL"):
            print(f"\nTo change to this directory in your shell, run:")
            print(f"cd {project_path}")
        else:
            print(f"Current working directory: {os.getcwd()}")

    except OSError as e:
        print(f"Error changing to project directory: {e}")
        sys.exit(1)


@projects.command()
@click.pass_context
def info(ctx):
    """Show information about the active project"""
    config = ctx.obj["config"]

    # Get the active project configuration
    project_config = get_active_project_config(config)
    if not project_config:
        print("No active project configured.")
        return

    print(f"Active Project: {project_config.name}")
    if project_config.description:
        print(f"Description: {project_config.description}")
    if project_config.project_directory:
        print(f"Project Directory: {project_config.project_directory}")
    if project_config.docker_compose_file:
        print(f"Docker Compose File: {project_config.docker_compose_file}")
    if project_config.data_directory:
        print(f"Data Directory: {project_config.data_directory}")
