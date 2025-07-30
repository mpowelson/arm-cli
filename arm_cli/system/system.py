import subprocess

import click
import docker
import inquirer

from arm_cli.system.setup_utils import setup_shell, setup_xhost, setup_data_directories


@click.group()
def system():
    """Manage the system this CLI is running on"""
    pass


@system.command()
def setup():
    """Generic setup (will be refined later)"""

    setup_xhost()

    setup_shell()

    # Setup data directories (may require sudo)
    if not setup_data_directories():
        print("Data directory setup was not completed.")
        print("You can run this setup again later with: arm-cli system setup")

    # Additional setup code can go here (e.g., starting containers, attaching, etc.)
    pass
