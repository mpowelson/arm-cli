from typing import Optional

import click
import inquirer
from arm_robotics_sdk import application, project, stacks


@click.group()
def stack():
    """Manage stacks in the active application"""
    pass


@stack.command("add")
@click.argument("catalog_id")
@click.option("--name", help="Instance name for the stack")
@click.pass_context
def add(ctx, catalog_id: str, name: Optional[str] = None):
    """Add a stack from the catalog to the active application"""
    try:
        active_path = project.get_active_project()
        if not active_path:
            print("No active application. Use 'arm app open <path>' first.")
            raise click.Abort()

        instance_id, stack_obj = stacks.add_instance_to_project(catalog_id, name)
        print(f"Added stack: {stack_obj.name} ({instance_id})")
    except Exception as e:
        print(f"Error adding stack: {e}")
        raise click.Abort()


@stack.command("remove")
@click.argument("instance_id", required=False)
@click.pass_context
def remove(ctx, instance_id: Optional[str] = None):
    """Remove a stack from the active application"""
    try:
        active_path = project.get_active_project()
        if not active_path:
            print("No active application. Use 'arm app open <path>' first.")
            raise click.Abort()

        # Load instances to show selection if no ID provided
        if not instance_id:
            instances, catalog_ids = stacks.load_instances(active_path)
            if not instances:
                print("No stacks in the application")
                return

            choices = [f"{stack.name} ({iid})" for iid, stack in instances.items()]
            questions = [
                inquirer.List(
                    "stack",
                    message="Select a stack to remove",
                    choices=choices,
                    carousel=True,
                )
            ]

            answers = inquirer.prompt(questions)
            if not answers:
                print("Cancelled")
                return

            # Extract instance ID from selection
            instance_id = answers["stack"].split("(")[-1].rstrip(")")

        stacks.remove_instance_from_project(instance_id)
        print(f"Removed stack: {instance_id}")
    except Exception as e:
        print(f"Error removing stack: {e}")
        raise click.Abort()


@stack.command("list")
@click.pass_context
def list_stacks(ctx):
    """List stacks in the active application"""
    try:
        active_path = project.get_active_project()
        if not active_path:
            print("No active application. Use 'arm app open <path>' first.")
            raise click.Abort()

        instances, catalog_ids = stacks.load_instances(active_path)
        if not instances:
            print("No stacks in the application")
            return

        print("Stacks in application:")
        for instance_id, stack_obj in instances.items():
            catalog_id = catalog_ids.get(instance_id, "unknown")
            print(f"  {stack_obj.name} ({instance_id})")
            print(f"    Catalog: {catalog_id}")
    except Exception as e:
        print(f"Error listing stacks: {e}")
        raise click.Abort()


@stack.command("configure")
@click.argument("instance_id", required=False)
@click.pass_context
def configure(ctx, instance_id: Optional[str] = None):
    """Configure a stack instance (interactive)"""
    try:
        active_path = project.get_active_project()
        if not active_path:
            print("No active application. Use 'arm app open <path>' first.")
            raise click.Abort()

        # Load instances
        instances, catalog_ids = stacks.load_instances(active_path)
        if not instances:
            print("No stacks in the application")
            return

        # If no instance ID provided, show selection
        if not instance_id:
            choices = [f"{stack.name} ({iid})" for iid, stack in instances.items()]
            questions = [
                inquirer.List(
                    "stack",
                    message="Select a stack to configure",
                    choices=choices,
                    carousel=True,
                )
            ]

            answers = inquirer.prompt(questions)
            if not answers:
                print("Cancelled")
                return

            instance_id = answers["stack"].split("(")[-1].rstrip(")")

        if instance_id not in instances:
            print(f"Stack instance not found: {instance_id}")
            return

        stack_obj = instances[instance_id]
        print(f"\nConfiguring: {stack_obj.name}")
        print(f"Instance ID: {instance_id}")
        print("\nCurrent settings:")
        if hasattr(stack_obj, "settings") and stack_obj.settings:
            for key, value in stack_obj.settings.model_dump().items():
                print(f"  {key}: {value}")
        else:
            print("  (No configurable settings)")

        print("\nNote: Interactive configuration coming soon.")
        print("For now, edit settings manually in .arm-robotics/stack_instances.json")
    except Exception as e:
        print(f"Error configuring stack: {e}")
        raise click.Abort()
