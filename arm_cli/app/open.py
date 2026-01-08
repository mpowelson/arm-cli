from pathlib import Path
from typing import Optional

import click
import inquirer

from arm_robotics_sdk import project


def _open(ctx, path: Optional[str] = None):
    """Open an existing ARM Robotics application
    
    If no path is provided, shows a list of recent projects to select from.
    """
    # If no path provided, show interactive selection from recent projects
    if path is None:
        try:
            recent = project.get_recent_projects()
            
            if not recent:
                print("No recent applications found.")
                print("Usage: arm app open <path>")
                return
            
            # Create choices for inquirer
            choices = []
            active_path = project.get_active_project()
            
            for proj_info in recent:
                active_indicator = " (active)" if proj_info.path == active_path else ""
                display = f"{proj_info.name}{active_indicator}"
                choices.append((display, proj_info.path))
            
            questions = [
                inquirer.List(
                    "project",
                    message="Select an application to open",
                    choices=choices,
                    carousel=True,
                )
            ]
            
            answers = inquirer.prompt(questions)
            if not answers:
                print("Cancelled")
                return
            
            path = answers["project"]
            
        except KeyboardInterrupt:
            print("\nCancelled")
            return
        except Exception as e:
            print(f"Error loading recent projects: {e}")
            raise click.Abort()
    
    path_obj = Path(path).resolve()
    
    try:
        info = project.open_project(path_obj)
        print(f"Opened application: {info.name}")
        print(f"Location: {info.path}")
        if info.description:
            print(f"Description: {info.description}")
    except Exception as e:
        print(f"Error opening application: {e}")
        raise click.Abort()


# Create the command object
open = click.command(name="open")(
    click.argument("path", type=click.Path(exists=True), required=False)(
        click.pass_context(_open)
    )
)

