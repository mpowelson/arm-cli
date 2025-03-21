import subprocess

import click
import docker
import inquirer

from arm_cli.system.setup_utils import setup_shell, setup_xhost


@click.group()
def system():
    """Manage the system this CLI is running on"""
    pass


@system.command()
def setup():
    """Generic setup (will be refined later)"""

    setup_xhost()

    setup_shell()

    # Additional setup code can go here (e.g., starting containers, attaching, etc.)
    pass
