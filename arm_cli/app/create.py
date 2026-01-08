from pathlib import Path
from typing import Optional

import click

from arm_robotics_sdk import project


def _create(ctx, path: str, name: Optional[str] = None, description: Optional[str] = None):
    """Create a new ARM Robotics application"""
    path_obj = Path(path).resolve()
    
    if not name:
        name = path_obj.name
    
    try:
        info = project.create_project(path_obj, name, description)
        print(f"Created application: {info.name}")
        print(f"Location: {info.path}")
        if info.description:
            print(f"Description: {info.description}")
    except Exception as e:
        print(f"Error creating application: {e}")
        raise click.Abort()


# Create the command object
create = click.command(name="create")(
    click.argument("path", type=click.Path())(
        click.option("--name", help="Name for the application")(
            click.option("--description", help="Description of the application")(
                click.pass_context(_create)
            )
        )
    )
)

