import click

# Import subcommands
import arm_cli.app.build
import arm_cli.app.connect
import arm_cli.app.create
import arm_cli.app.disconnect
import arm_cli.app.info
import arm_cli.app.open
import arm_cli.app.stack

# Get command objects
build = arm_cli.app.build.build
connect = arm_cli.app.connect.connect
create = arm_cli.app.create.create
disconnect = arm_cli.app.disconnect.disconnect
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
app.add_command(connect)
app.add_command(disconnect)
app.add_command(build)

