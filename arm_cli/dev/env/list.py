import click

from arm_cli.config import get_available_projects


def _list(ctx):
    """List available development environments"""
    config = ctx.obj["config"]

    available = get_available_projects(config)

    if not available:
        print("No development environments configured")
        print("Use 'arm dev env create' to create one")
        return

    print("Development environments:")
    for proj in available:
        active_marker = " (active)" if proj.path == config.active_project else ""
        print(f"  {proj.name}{active_marker}")
        print(f"    Path: {proj.path}")


# Create the command object
list = click.command(name="list")(click.pass_context(_list))
