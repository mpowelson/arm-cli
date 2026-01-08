import click

from arm_cli.config import get_active_project_config


def _add(ctx, name: str, target: str, alias_type: str = "cdp"):
    """Add an alias to the active environment

    Types:
        cdp: Change directory shortcut (default)
        custom: Custom shell alias
    """
    config = ctx.obj["config"]

    project_config = get_active_project_config(config)
    if not project_config:
        print("No active development environment")
        print("Use 'arm dev env activate' to activate one first")
        raise click.Abort()

    print(f"Adding alias '{name}' to environment: {project_config.name}")
    print(f"Type: {alias_type}")
    print(f"Target: {target}")
    print("\nNote: Alias storage and shell integration coming soon.")
    print("For now, manually add to your shell config:")

    if alias_type == "cdp":
        print(f"  alias {name}='cd {target}'")
    else:
        print(f"  alias {name}='{target}'")


# Create the command object
add = click.command(name="add")(
    click.argument("name")(
        click.argument("target")(
            click.option(
                "--type",
                "alias_type",
                type=click.Choice(["cdp", "custom"]),
                default="cdp",
                help="Type of alias",
            )(click.pass_context(_add))
        )
    )
)
