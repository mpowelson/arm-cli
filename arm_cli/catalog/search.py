from typing import Optional

import click
from arm_robotics_sdk.catalog import stack


def _search(ctx, pattern: Optional[str] = None):
    """Search for stacks in the catalog

    If no pattern provided, prompts for search term.
    """
    try:
        # Prompt for pattern if not provided
        if pattern is None:
            pattern = click.prompt("Enter search pattern", type=str)

        results = stack.search_stacks(pattern)

        if not results:
            print(f"No stacks found matching '{pattern}'")
            return

        print(f"Stacks matching '{pattern}':")
        for channel_name, channel_stacks in results.items():
            if channel_stacks:
                print(f"\n{channel_name}:")
                for stack_entry in channel_stacks:
                    stack_id = f"{channel_name}:{stack_entry.name}"
                    print(f"  {stack_id}")
                    if hasattr(stack_entry, "summary") and stack_entry.summary:
                        if hasattr(stack_entry.summary, "description"):
                            print(f"    {stack_entry.summary.description}")
    except click.Abort:
        raise
    except Exception as e:
        print(f"Error searching catalog: {e}")
        raise click.Abort()


# Create the command object
search = click.command(name="search")(
    click.argument("pattern", required=False)(click.pass_context(_search))
)
