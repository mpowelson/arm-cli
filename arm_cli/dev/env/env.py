import click

# Import commands (adapted from projects/)
import arm_cli.dev.env.activate
import arm_cli.dev.env.create
import arm_cli.dev.env.info
import arm_cli.dev.env.list
import arm_cli.dev.env.remove

# Get command objects
activate = arm_cli.dev.env.activate.activate
create = arm_cli.dev.env.create.create
info = arm_cli.dev.env.info.info
list_cmd = arm_cli.dev.env.list.list
remove = arm_cli.dev.env.remove.remove


@click.group()
def env():
    """Manage development environments"""
    pass


# Register all env commands
env.add_command(create)
env.add_command(activate)
env.add_command(list_cmd, name="list")
env.add_command(info)
env.add_command(remove)
