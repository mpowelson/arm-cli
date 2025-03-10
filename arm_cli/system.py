import click
import docker
import inquirer
import subprocess

@click.group()
def system():
    """Manage the system this CLI is running on"""
    pass


@system.command()
def setup():
    """Generic setup (will be refined later)"""
    try:
        # Ensure xhost allows local Docker connections
        print("Setting up X11 access for Docker containers...")
        subprocess.run(["xhost", "+local:docker"], check=True)
        print("xhost configured successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error configuring xhost: {e}")

    # Additional setup code can go here (e.g., starting containers, attaching, etc.)
    pass