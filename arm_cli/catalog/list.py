from typing import Optional

import click
from arm_robotics_sdk.catalog import stack


def _list(ctx, channel: Optional[str] = None):
    """List stacks from the catalog"""
    try:
        all_stacks = stack.get_stacks()

        if not all_stacks:
            print("No stacks available in catalog")
            return

        # Filter by channel if specified
        if channel:
            if channel not in all_stacks:
                print(f"Channel '{channel}' not found")
                return
            stacks_to_show = {channel: all_stacks[channel]}
        else:
            stacks_to_show = all_stacks

        print("Available stacks:")
        for channel_name, channel_stacks in stacks_to_show.items():
            print(f"\n{channel_name}:")
            for stack_entry in channel_stacks:
                stack_id = f"{channel_name}:{stack_entry.name}"
                print(f"  {stack_id}")
                if hasattr(stack_entry, "summary") and stack_entry.summary:
                    if hasattr(stack_entry.summary, "description"):
                        print(f"    {stack_entry.summary.description}")
    except Exception as e:
        print(f"Error listing catalog: {e}")
        raise click.Abort()


# Create the command object
list = click.command(name="list")(
    click.option("--channel", help="Filter by channel")(click.pass_context(_list))
)
