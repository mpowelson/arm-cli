import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

import click
import inquirer

from arm_cli.config import (
    activate_project,
    add_project_to_list,
    copy_default_project_config,
    get_active_project_config,
    get_available_projects,
    load_project_config,
    remove_project_from_list,
    save_config,
)


@click.group()
def projects():
    """Manage ARM projects"""
    pass


@projects.command()
@click.argument("project_path", type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option("--name", help="Name for the project (defaults to directory name)")
@click.pass_context
def init(ctx, project_path: str, name: Optional[str] = None):
    """Initialize a new project from an existing directory"""
    config = ctx.obj["config"]

    project_path_obj = Path(project_path).resolve()

    if name is None:
        name = project_path_obj.name

    # Check if project config already exists
    project_config_file = project_path_obj / "project_config.json"

    if project_config_file.exists():
        print(f"Project config already exists at {project_config_file}")
        print("Loading existing project configuration...")
        project_config = load_project_config(str(project_config_file))
    else:
        # Copy default config and customize it
        try:
            default_config_path = copy_default_project_config()
            with open(default_config_path, "r") as f:
                import json

                default_data = json.load(f)

            # Update with project-specific information
            default_data["name"] = name
            default_data["project_directory"] = str(project_path_obj)

            # Save the new project config
            with open(project_config_file, "w") as f:
                json.dump(default_data, f, indent=2)

            project_config = load_project_config(str(project_config_file))
            print(f"Created new project configuration at {project_config_file}")

        except Exception as e:
            print(f"Error creating project configuration: {e}")
            sys.exit(1)

    # Add to available projects and set as active
    add_project_to_list(config, str(project_config_file), project_config.name)
    save_config(config)

    print(f"Project '{project_config.name}' initialized and set as active")
    print(f"Project directory: {project_config.project_directory}")


@projects.command()
@click.argument("project", required=False)
@click.pass_context
def activate(ctx, project: Optional[str] = None):
    """Activate a project from available projects"""
    config = ctx.obj["config"]

    # If no project specified, show interactive list
    if project is None:
        available_projects = get_available_projects(config)

        if not available_projects:
            print("No projects available. Use 'arm-cli projects init <path>' to add a project.")
            return

        # Create choices for inquirer
        choices = []
        for proj in available_projects:
            active_indicator = " *" if proj.path == config.active_project else ""
            choices.append(f"{proj.name}{active_indicator}")

        # Create the question
        questions = [
            inquirer.List(
                "project", message="Select a project to activate", choices=choices, carousel=True
            )
        ]

        try:
            answers = inquirer.prompt(questions)
            if answers is None:
                print("Cancelled.")
                return

            # Extract project name (remove the active indicator if present)
            selected_choice = answers["project"]
            project = selected_choice.replace(" *", "")

        except KeyboardInterrupt:
            print("\nCancelled.")
            return

    # Try to activate the project
    # At this point, project is guaranteed to be a string
    assert project is not None  # type guard
    project_config = activate_project(config, project)

    if project_config:
        print(f"Activated project: {project_config.name}")
        print(f"Project directory: {project_config.project_directory}")
    else:
        print(f"Project '{project}' not found in available projects")
        print("\nAvailable projects:")
        available_projects = get_available_projects(config)
        if available_projects:
            for i, proj in enumerate(available_projects, 1):
                print(f"  {i}. {proj.name} ({proj.path})")
        else:
            print("  No projects available. Use 'arm-cli projects init <path>' to add a project.")


@projects.command()
@click.pass_context
def list(ctx):
    """List all available projects"""
    config = ctx.obj["config"]
    available_projects = get_available_projects(config)

    if not available_projects:
        print("No projects available. Use 'arm-cli projects init <path>' to add a project.")
        return

    print("Available Projects:")
    for i, project in enumerate(available_projects, 1):
        active_indicator = " *" if project.path == config.active_project else ""
        print(f"  {i}. {project.name}{active_indicator}")
        print(f"     Path: {project.path}")
        print()


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


@projects.command()
@click.argument("project", required=False)
@click.pass_context
def remove(ctx, project: Optional[str] = None):
    """Remove a project from available projects"""
    config = ctx.obj["config"]

    # If no project specified, show interactive list
    if project is None:
        available_projects = get_available_projects(config)

        if not available_projects:
            print("No projects available to remove.")
            return

        # Create choices for inquirer
        choices = []
        for proj in available_projects:
            active_indicator = " *" if proj.path == config.active_project else ""
            choices.append(f"{proj.name}{active_indicator}")

        # Create the question
        questions = [
            inquirer.List(
                "project", message="Select a project to remove", choices=choices, carousel=True
            )
        ]

        try:
            answers = inquirer.prompt(questions)
            if answers is None:
                print("Cancelled.")
                return

            # Extract project name (remove the active indicator if present)
            selected_choice = answers["project"]
            project = selected_choice.replace(" *", "")

        except KeyboardInterrupt:
            print("\nCancelled.")
            return

    # Try to remove the project
    # At this point, project is guaranteed to be a string
    assert project is not None  # type guard

    # Check if this is the active project
    available_projects = get_available_projects(config)
    is_active = False
    for proj in available_projects:
        if proj.name.lower() == project.lower():
            is_active = proj.path == config.active_project
            break

    # Confirm removal, especially for active project
    if is_active:
        confirm_questions = [
            inquirer.Confirm(
                "confirm",
                message=f"Are you sure you want to remove the active project '{project}'? This will clear the active project.",
                default=False,
            )
        ]

        try:
            confirm_answers = inquirer.prompt(confirm_questions)
            if confirm_answers is None or not confirm_answers["confirm"]:
                print("Removal cancelled.")
                return
        except KeyboardInterrupt:
            print("\nCancelled.")
            return
    else:
        confirm_questions = [
            inquirer.Confirm(
                "confirm",
                message=f"Are you sure you want to remove project '{project}'?",
                default=False,
            )
        ]

        try:
            confirm_answers = inquirer.prompt(confirm_questions)
            if confirm_answers is None or not confirm_answers["confirm"]:
                print("Removal cancelled.")
                return
        except KeyboardInterrupt:
            print("\nCancelled.")
            return

    # Remove the project
    if remove_project_from_list(config, project):
        save_config(config)
        print(f"Removed project: {project}")
        if is_active:
            print("Active project has been cleared.")
    else:
        print(f"Project '{project}' not found in available projects")
        print("\nAvailable projects:")
        available_projects = get_available_projects(config)
        if available_projects:
            for i, proj in enumerate(available_projects, 1):
                print(f"  {i}. {proj.name} ({proj.path})")
        else:
            print("  No projects available.")
