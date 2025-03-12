import click
import subprocess
import sys
import os


@click.group()
def self():
    """Manage the CLI itself"""
    pass


@self.command()
@click.option(
    "--source",
    default=".",
    type=click.Path(exists=True),
    help="Install from a local source path",
    show_default=True,
)
def update(source):
    """Update arm-cli from PyPI or source"""
    if source:
        print(f"Installing arm-cli from source at {source}...")

        # Clear Python import cache
        print("Clearing Python caches...")
        subprocess.run(["rm", "-rf", os.path.expanduser("~/.cache/pip")])
        subprocess.run(["python", "-c", "import importlib; importlib.invalidate_caches()"])

        # Install from the provided source path
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", source], check=True)
        print(f"arm-cli installed from source at {source} successfully!")
    else:
        print("Updating arm-cli from PyPI...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "arm-cli"], check=True)
        print("arm-cli updated successfully!")
