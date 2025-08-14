from typing import Optional

import click
import inquirer

from arm_cli.config import activate_project, get_available_projects


def _activate(ctx, project: Optional[str] = None):
    """Activate a project from available projects"""
    config = ctx.obj["config"]

    # If no project specified, show interactive list
    if project is None:
        available_projects = get_available_projects(config)

        if not available_projects:
            print("No projects available. Use 'arm-cli projects init <path>' to add a project.")
            return

        # Create choices for inquirer
        choices = []
        for proj in available_projects:
            active_indicator = " *" if proj.path == config.active_project else ""
            choices.append(f"{proj.name}{active_indicator}")

        # Create the question
        questions = [
            inquirer.List(
                "project", message="Select a project to activate", choices=choices, carousel=True
            )
        ]

        try:
            answers = inquirer.prompt(questions)
            if answers is None:
                print("Cancelled.")
                return

            # Extract project name (remove the active indicator if present)
            selected_choice = answers["project"]
            project = selected_choice.replace(" *", "")

        except KeyboardInterrupt:
            print("\nCancelled.")
            return

    # Try to activate the project
    # At this point, project is guaranteed to be a string
    assert project is not None  # type guard
    project_config = activate_project(config, project)

    if project_config:
        print(f"Activated project: {project_config.name}")
        print(f"Project directory: {project_config.project_directory}")
    else:
        print(f"Project '{project}' not found in available projects")
        print("\nAvailable projects:")
        available_projects = get_available_projects(config)
        if available_projects:
            for i, proj in enumerate(available_projects, 1):
                print(f"  {i}. {proj.name} ({proj.path})")
        else:
            print("  No projects available. Use 'arm-cli projects init <path>' to add a project.")


# Create the command object
activate = click.command(name="activate")(
    click.argument("project", required=False)(click.pass_context(_activate))
)
