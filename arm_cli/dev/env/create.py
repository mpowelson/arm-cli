import json
from pathlib import Path
from typing import Optional

import click

from arm_cli.config import add_project_to_list, get_config_dir, load_project_config, save_config


def _create(ctx, name: str, directory: Optional[str] = None):
    """Create a new development environment"""
    config = ctx.obj["config"]

    # For now, reuse the existing project config structure
    # Future enhancement: create dedicated environment config structure
    if directory:
        project_path_obj = Path(directory).resolve()

        # Create a simple config file in the directory
        config_file = project_path_obj / f"{name}_env.json"
        if config_file.exists():
            print(f"Environment config already exists: {config_file}")
            return

        # Create shell config file
        shell_dir = get_config_dir() / "shell"
        shell_dir.mkdir(parents=True, exist_ok=True)
        shell_config_path = shell_dir / f"{name}.sh"

        # Create shell config template
        shell_template = f"""# Shell config for environment: {name}
# This file is sourced when this environment is active.
# Add your aliases, functions, and environment variables here.

# Example: Change to workspace directory
# alias cdw='cd {project_path_obj}'

# Example: Set environment variables
# export PROJECT_ROOT="{project_path_obj}"

# Example: Custom aliases
# alias build='arm-cli app build'
"""

        with open(shell_config_path, "w") as f:
            f.write(shell_template)

        # Create basic config
        env_config = {
            "name": name,
            "description": f"Development environment: {name}",
            "project_directory": str(project_path_obj),
            "shell_config_path": str(shell_config_path),
        }

        with open(config_file, "w") as f:
            json.dump(env_config, f, indent=2)

        # Add to available projects list
        add_project_to_list(config, str(config_file), name)
        save_config(config)

        print(f"Created development environment: {name}")
        print(f"Config file: {config_file}")
        print(f"Directory: {project_path_obj}")
        print(f"\nShell configuration file created at: {shell_config_path}")
        print("Edit this file to add custom aliases, environment variables, or functions.")
        print(f"Example: alias cdw='cd {project_path_obj}'")
    else:
        print("Error: --directory is required")
        print("Usage: arm dev env create <name> --directory <path>")
        raise click.Abort()


# Create the command object
create = click.command(name="create")(
    click.argument("name")(
        click.option("--directory", help="Directory for this environment")(
            click.pass_context(_create)
        )
    )
)
