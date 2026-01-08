import click

# Import subgroups
import arm_cli.dev.env.env

# Get subgroup objects
env = arm_cli.dev.env.env.env


@click.group()
def dev():
    """Manage developer environments"""
    pass


# Register subgroups
dev.add_command(env)
