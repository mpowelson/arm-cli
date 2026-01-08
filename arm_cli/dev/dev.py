import click

# Import subgroups
import arm_cli.dev.alias.alias
import arm_cli.dev.env.env

# Get subgroup objects
alias = arm_cli.dev.alias.alias.alias
env = arm_cli.dev.env.env.env


@click.group()
def dev():
    """Manage developer environments"""
    pass


# Register subgroups
dev.add_command(env)
dev.add_command(alias)
