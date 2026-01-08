import click

from arm_cli.config import get_active_project_config


def _info(ctx):
    """Show information about the active development environment"""
    config = ctx.obj["config"]

    project_config = get_active_project_config(config)

    if not project_config:
        print("No active development environment")
        print("Use 'arm dev env activate' to activate one")
        return

    print(f"Active environment: {project_config.name}")

    if project_config.description:
        print(f"Description: {project_config.description}")

    resolved_dir = project_config.get_resolved_project_directory(
        getattr(project_config, "_config_file_path", None)
    )
    if resolved_dir:
        print(f"Directory: {resolved_dir}")


# Create the command object
info = click.command(name="info")(click.pass_context(_info))
