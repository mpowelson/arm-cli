import click

# Import subcommands
import arm_cli.app.build
import arm_cli.app.connection
import arm_cli.app.create
import arm_cli.app.info
import arm_cli.app.open
import arm_cli.app.stack

# Get command objects
build = arm_cli.app.build.build
connection = arm_cli.app.connection.connection
create = arm_cli.app.create.create
info = arm_cli.app.info.info
open_cmd = arm_cli.app.open.open
stack = arm_cli.app.stack.stack


@click.group()
def app():
    """Manage ARM Robotics applications"""
    pass


# Register all app commands
app.add_command(create)
app.add_command(open_cmd, name="open")
app.add_command(info)
app.add_command(stack)
app.add_command(connection)
app.add_command(build)
