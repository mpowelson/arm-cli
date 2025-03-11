import click
from arm_cli.container import container
from arm_cli.system.system import system

@click.group()
@click.version_option()
def cli():
    """Experimental CLI for deploying robotic applications"""
    pass

# Add the container management commands as a sub-group
cli.add_command(container)
cli.add_command(system)

if __name__ == "__main__":
    cli()