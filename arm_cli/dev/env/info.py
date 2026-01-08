import os

import click

from arm_cli.config import get_active_project_config


def _info(ctx, shell_config: bool = False):
    """Show information about the active development environment"""
    config = ctx.obj["config"]

    project_config = get_active_project_config(config)

    if not project_config:
        if not shell_config:
            print("No active development environment")
            print("Use 'arm dev env activate' to activate one")
        return

    # If --shell-config flag is set, only output the shell config path
    if shell_config:
        shell_config_path = project_config.shell_config_path
        if shell_config_path:
            # Expand ~ to full path
            expanded_path = os.path.expanduser(shell_config_path)
            print(expanded_path)
        return

    # Normal info display
    print(f"Active environment: {project_config.name}")

    if project_config.description:
        print(f"Description: {project_config.description}")

    resolved_dir = project_config.get_resolved_project_directory(
        getattr(project_config, "_config_file_path", None)
    )
    if resolved_dir:
        print(f"Directory: {resolved_dir}")

    if project_config.shell_config_path:
        print(f"Shell config: {project_config.shell_config_path}")


# Create the command object
info = click.command(name="info")(
    click.option(
        "--shell-config",
        is_flag=True,
        help="Output only the shell config path (for shell script integration)",
    )(click.pass_context(_info))
)
