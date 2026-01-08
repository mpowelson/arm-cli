import click

from arm_cli.config import get_active_project_config


def _list(ctx):
    """List aliases in the active environment"""
    config = ctx.obj["config"]

    project_config = get_active_project_config(config)
    if not project_config:
        print("No active development environment")
        print("Use 'arm dev env activate' to activate one first")
        return

    print(f"Aliases for environment: {project_config.name}")
    print("\nNote: Alias storage coming soon.")
    print("Aliases will be stored per-environment and activated automatically.")


# Create the command object
list = click.command(name="list")(click.pass_context(_list))
