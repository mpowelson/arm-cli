import click

from arm_cli.config import get_active_project_config


def _remove(ctx, name: str):
    """Remove an alias from the active environment"""
    config = ctx.obj["config"]

    project_config = get_active_project_config(config)
    if not project_config:
        print("No active development environment")
        print("Use 'arm dev env activate' to activate one first")
        raise click.Abort()

    print(f"Removing alias '{name}' from environment: {project_config.name}")
    print("\nNote: Alias storage coming soon.")


# Create the command object
remove = click.command(name="remove")(click.argument("name")(click.pass_context(_remove)))
