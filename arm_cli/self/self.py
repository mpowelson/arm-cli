import os
import subprocess
import sys

import click
from click.core import ParameterSource

from arm_cli.config import save_config


@click.group()
def self():
    """Manage the CLI itself"""
    pass


@self.command()
@click.option(
    "--source",
    default=None,
    type=click.Path(exists=True),
    help="Install from a local source path (defaults to current directory if specified without value)",
)
@click.option("-f", "--force", is_flag=True, help="Skip confirmation prompts")
@click.pass_context
def update(ctx, source, force):
    config = ctx.obj["config"]  # noqa: F841 - config available for future use
    """Update arm-cli from PyPI or source"""
    if source is None and ctx.get_parameter_source("source") == ParameterSource.COMMANDLINE:
        source = "."

    if source:
        print(f"Installing arm-cli from source at {source}...")

        if not force:
            if not click.confirm(
                "Do you want to install arm-cli from source? This will clear pip " "cache."
            ):
                print("Update cancelled.")
                return

        # Clear Python import cache
        print("Clearing Python caches...")
        subprocess.run(["rm", "-rf", os.path.expanduser("~/.cache/pip")])
        subprocess.run(["python", "-c", "import importlib; importlib.invalidate_caches()"])

        # Install from the provided source path
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", source], check=True)
        print(f"arm-cli installed from source at {source} successfully!")
    else:
        print("Updating arm-cli from PyPI...")

        if not force:
            if not click.confirm("Do you want to update arm-cli from PyPI?"):
                print("Update cancelled.")
                return

        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "arm-cli"], check=True)
        print("arm-cli updated successfully!")


@self.command()
@click.option("--project", help="Set the active project")
@click.pass_context
def config(ctx, project):
    """Manage CLI configuration"""
    config = ctx.obj["config"]

    if project is not None:
        config.active_project = project
        save_config(config)
        print(f"Active project set to: {project}")
    else:
        print(f"Active project: {config.active_project}")
        print("Use --project to set a new active project")
