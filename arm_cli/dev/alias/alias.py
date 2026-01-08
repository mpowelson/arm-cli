import click

# Import commands
import arm_cli.dev.alias.add
import arm_cli.dev.alias.list
import arm_cli.dev.alias.remove

# Get command objects
add = arm_cli.dev.alias.add.add
list_cmd = arm_cli.dev.alias.list.list
remove = arm_cli.dev.alias.remove.remove


@click.group()
def alias():
    """Manage aliases in development environments"""
    pass


# Register all alias commands
alias.add_command(add)
alias.add_command(list_cmd, name="list")
alias.add_command(remove)
