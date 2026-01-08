import click

from arm_robotics_sdk import project


def _info(ctx):
    """Show information about the active application"""
    try:
        active_path = project.get_active_project()
        if not active_path:
            print("No active application")
            print("Use 'arm-cli app open <path>' to open an application")
            return
        
        # Get project info
        info = project.open_project(active_path)
        print(f"Active application: {info.name}")
        print(f"Location: {info.path}")
        if info.description:
            print(f"Description: {info.description}")
    except Exception as e:
        print(f"Error getting application info: {e}")
        raise click.Abort()


# Create the command object
info = click.command(name="info")(
    click.pass_context(_info)
)

