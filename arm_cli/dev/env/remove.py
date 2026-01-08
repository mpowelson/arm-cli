from typing import Optional

import click
import inquirer

from arm_cli.config import get_available_projects, remove_project_from_list, save_config


def _remove(ctx, env: Optional[str] = None):
    """Remove a development environment from the list"""
    config = ctx.obj["config"]

    available = get_available_projects(config)

    if not available:
        print("No development environments configured")
        return

    # If no env specified, show interactive selection
    if env is None:
        choices = [proj.name for proj in available]

        questions = [
            inquirer.List(
                "env",
                message="Select an environment to remove",
                choices=choices,
                carousel=True,
            )
        ]

        try:
            answers = inquirer.prompt(questions)
            if answers is None:
                print("Cancelled.")
                return
            env = answers["env"]
        except KeyboardInterrupt:
            print("\nCancelled.")
            return

    # Remove the environment
    if remove_project_from_list(config, env):
        save_config(config)
        print(f"Removed environment: {env}")
    else:
        print(f"Environment not found: {env}")


# Create the command object
remove = click.command(name="remove")(
    click.argument("env", required=False)(click.pass_context(_remove))
)
