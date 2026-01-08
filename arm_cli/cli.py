import click

from arm_cli import __version__
from arm_cli.app.app import app
from arm_cli.catalog.catalog import catalog
from arm_cli.config import load_config
from arm_cli.container.container import container
from arm_cli.deploy.deploy import deploy
from arm_cli.dev.dev import dev
from arm_cli.self.self import self
from arm_cli.system.system import system


@click.version_option(version=__version__)
@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.pass_context
def cli(ctx):
    """CLI for ARM Robotics framework - manage applications, catalogs, and deployments"""
    # Load config and store in context
    ctx.ensure_object(dict)
    ctx.obj["config"] = load_config()


# Add command groups
cli.add_command(app)
cli.add_command(catalog)
cli.add_command(deploy)
cli.add_command(dev)
cli.add_command(container)
cli.add_command(system)
cli.add_command(self)

if __name__ == "__main__":
    cli()
