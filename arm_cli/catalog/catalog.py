import click

# Import subcommands
import arm_cli.catalog.fetch
import arm_cli.catalog.info
import arm_cli.catalog.list
import arm_cli.catalog.search

# Get command objects
fetch = arm_cli.catalog.fetch.fetch
info = arm_cli.catalog.info.info
list_cmd = arm_cli.catalog.list.list
search = arm_cli.catalog.search.search


@click.group()
def catalog():
    """Browse and search the stack catalog"""
    pass


# Register all catalog commands
catalog.add_command(search)
catalog.add_command(list_cmd, name="list")
catalog.add_command(info)
catalog.add_command(fetch)
