# Copy from projects/activate.py with updated terminology
from typing import Optional

import click
import inquirer

from arm_cli.config import (
    activate_project,
    get_active_project_config,
    get_available_projects,
    print_available_projects,
    print_no_projects_message,
)


def _activate(ctx, env: Optional[str] = None):
    """Activate a development environment"""
    config = ctx.obj["config"]

    # If no env specified, show interactive list
    if env is None:
        available_projects = get_available_projects(config)

        if not available_projects:
            print("No environments available. Setting up default...")
            project_config = get_active_project_config(config)
            if project_config:
                print(f"Activated default environment: {project_config.name}")
                resolved_dir = project_config.get_resolved_project_directory(
                    getattr(project_config, "_config_file_path", None)
                )
                print(f"Directory: {resolved_dir}")
            else:
                print("Failed to set up default environment.")
                print("Use 'arm dev env create' to create an environment.")
            return

        # Create choices for inquirer
        choices = []
        for proj in available_projects:
            active_indicator = " *" if proj.path == config.active_project else ""
            choices.append(f"{proj.name}{active_indicator}")

        # Create the question
        questions = [
            inquirer.List(
                "env",
                message="Select an environment to activate",
                choices=choices,
                carousel=True,
            )
        ]

        try:
            answers = inquirer.prompt(questions)
            if answers is None:
                print("Cancelled.")
                return

            # Extract env name (remove the active indicator if present)
            selected_choice = answers["env"]
            env = selected_choice.replace(" *", "")
            if env is None:
                raise RuntimeError("Environment name cannot be None")

        except KeyboardInterrupt:
            print("\nCancelled.")
            return

    # Try to activate the environment
    project_config = activate_project(config, env)

    if project_config:
        print(f"Activated environment: {project_config.name}")
        resolved_dir = project_config.get_resolved_project_directory(
            getattr(project_config, "_config_file_path", None)
        )
        print(f"Directory: {resolved_dir}")
    else:
        print(f"Environment '{env}' not found")
        print_available_projects(config)


# Create the command object
activate = click.command(name="activate")(
    click.argument("env", required=False)(click.pass_context(_activate))
)
