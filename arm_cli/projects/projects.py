import click

from arm_cli.projects import activate, info, init, list, remove


@click.group()
def projects():
    """Manage ARM projects"""
    pass


# Register all project commands
projects.add_command(init.init)
projects.add_command(activate.activate)
projects.add_command(list.list)
projects.add_command(info.info)
projects.add_command(remove.remove)
