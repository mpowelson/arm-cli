import click

from arm_cli.config import get_active_project_config


@click.command()
@click.pass_context
def info(ctx):
    """Show information about the active project"""
    config = ctx.obj["config"]

    # Get the active project configuration
    project_config = get_active_project_config(config)
    if not project_config:
        print("No active project configured.")
        return

    print(f"Active Project: {project_config.name}")
    if project_config.description:
        print(f"Description: {project_config.description}")
    if project_config.project_directory:
        print(f"Project Directory: {project_config.project_directory}")
    if project_config.docker_compose_file:
        print(f"Docker Compose File: {project_config.docker_compose_file}")
    if project_config.data_directory:
        print(f"Data Directory: {project_config.data_directory}")
