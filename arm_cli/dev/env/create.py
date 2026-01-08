import json
from pathlib import Path
from typing import Optional

import click

from arm_cli.config import add_project_to_list, load_project_config, save_config


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

        # Create basic config
        env_config = {
            "name": name,
            "description": f"Development environment: {name}",
            "project_directory": str(project_path_obj),
        }

        with open(config_file, "w") as f:
            json.dump(env_config, f, indent=2)

        # Add to available projects list
        add_project_to_list(config, str(config_file), name)
        save_config(config)

        print(f"Created development environment: {name}")
        print(f"Config file: {config_file}")
        print(f"Directory: {project_path_obj}")
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
