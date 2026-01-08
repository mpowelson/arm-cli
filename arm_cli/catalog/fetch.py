from typing import Optional

import click
import inquirer
from arm_robotics_sdk.catalog import stack


def _fetch(ctx, stack_id: Optional[str] = None):
    """Fetch a stack repository locally

    If no stack_id provided, shows interactive selection.
    """
    try:
        # Interactive mode if no stack_id
        if stack_id is None:
            all_stacks = stack.get_stacks()

            if not all_stacks:
                print("No stacks available in catalog")
                return

            # Build list of stacks that aren't fetched yet
            unfetched_stacks = []
            for channel_name, channel_stacks in all_stacks.items():
                for stack_entry in channel_stacks:
                    sid = f"{channel_name}:{stack_entry.name}"
                    is_fetched = stack.is_stack_fetched(sid)

                    if not is_fetched:
                        desc = ""
                        if hasattr(stack_entry, "summary") and stack_entry.summary:
                            if hasattr(stack_entry.summary, "description"):
                                desc = f" - {stack_entry.summary.description}"
                        unfetched_stacks.append((f"{sid}{desc}", sid))

            if not unfetched_stacks:
                print("All stacks are already fetched locally")
                return

            questions = [
                inquirer.List(
                    "stack",
                    message="Select a stack to fetch",
                    choices=unfetched_stacks,
                    carousel=True,
                )
            ]

            answers = inquirer.prompt(questions)
            if not answers:
                print("Cancelled")
                return

            stack_id = answers["stack"]

        # Check if already fetched
        if stack.is_stack_fetched(stack_id):
            print(f"Stack {stack_id} is already fetched locally")
            return

        print(f"Fetching {stack_id}...")
        stack.fetch_stack(stack_id)
        print(f"Successfully fetched {stack_id}")

    except KeyboardInterrupt:
        print("\nCancelled")
    except Exception as e:
        print(f"Error fetching stack: {e}")
        raise click.Abort()


# Create the command object
fetch = click.command(name="fetch")(
    click.argument("stack_id", required=False)(click.pass_context(_fetch))
)
