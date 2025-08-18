import click
import inquirer

from arm_cli.config import load_config
from arm_cli.settings import get_setting, load_settings, save_settings, set_setting


@click.group()
def config():
    """Manage CLI configuration settings"""
    pass


@config.command("show")
@click.pass_context
def show_config(ctx):
    """Show current configuration settings"""
    config = ctx.obj["config"]
    settings = load_settings()

    print("Current CLI Configuration:")
    print(f"  Inquirer Page Size: {settings.inquirer_page_size}")
    print(f"  Active Project: {config.active_project or 'None'}")
    print(f"  Available Projects: {len(config.available_projects)}")


@config.command("set-page-size")
@click.argument("size", type=int)
@click.pass_context
def set_page_size(ctx, size):
    """Set the inquirer page size for interactive menus"""
    if size < 1:
        print("Error: Page size must be at least 1")
        return

    settings = load_settings()
    old_size = settings.inquirer_page_size
    settings.inquirer_page_size = size
    save_settings(settings)

    print(f"Inquirer page size updated: {old_size} → {size}")


@config.command("interactive")
@click.pass_context
def interactive_config(ctx):
    """Configure settings interactively"""
    settings = load_settings()

    questions = [
        inquirer.Text(
            "page_size",
            message="Enter inquirer page size (number of items shown in menus)",
            default=str(settings.inquirer_page_size),
            validate=lambda _, x: x.isdigit() and int(x) > 0 or "Please enter a positive number",
        )
    ]

    try:
        answers = inquirer.prompt(questions)
        if answers is None:
            print("Configuration cancelled.")
            return

        new_page_size = int(answers["page_size"])
        if new_page_size != settings.inquirer_page_size:
            settings.inquirer_page_size = new_page_size
            save_settings(settings)
            print(f"Inquirer page size updated to: {new_page_size}")
        else:
            print("No changes made.")

    except KeyboardInterrupt:
        print("\nConfiguration cancelled.")
