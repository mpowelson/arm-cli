from typing import Optional

import click
import inquirer
from arm_robotics_sdk.catalog import stack


def _info(ctx, stack_id: Optional[str] = None):
    """Show detailed information about a stack

    If no stack_id provided, shows interactive selection.
    """
    try:
        # Interactive mode if no stack_id
        if stack_id is None:
            all_stacks = stack.get_stacks()

            if not all_stacks:
                print("No stacks available in catalog")
                return

            # Build list of all stacks
            stack_choices = []
            for channel_name, channel_stacks in all_stacks.items():
                for stack_entry in channel_stacks:
                    sid = f"{channel_name}:{stack_entry.name}"
                    desc = ""
                    if hasattr(stack_entry, "summary") and stack_entry.summary:
                        if hasattr(stack_entry.summary, "description"):
                            desc = f" - {stack_entry.summary.description}"
                    stack_choices.append((f"{sid}{desc}", sid))

            if not stack_choices:
                print("No stacks available")
                return

            questions = [
                inquirer.List(
                    "stack",
                    message="Select a stack to view info",
                    choices=stack_choices,
                    carousel=True,
                )
            ]

            answers = inquirer.prompt(questions)
            if not answers:
                print("Cancelled")
                return

            stack_id = answers["stack"]

        entry, channel = stack.get_stack(stack_id)

        print(f"Stack: {stack_id}")
        print(f"Channel: {channel}")

        if hasattr(entry, "summary") and entry.summary:
            summary = entry.summary
            if hasattr(summary, "description") and summary.description:
                print(f"Description: {summary.description}")
            if hasattr(summary, "category") and summary.category:
                print(f"Category: {summary.category}")

        # Show more details if available
        if hasattr(entry, "repo") and entry.repo:
            repo = entry.repo
            if hasattr(repo, "type"):
                print(f"Repository type: {repo.type}")
            if hasattr(repo, "url") and repo.url:
                print(f"URL: {repo.url}")

        # Check if fetched
        is_fetched = stack.is_stack_fetched(stack_id)
        print(f"Fetched locally: {is_fetched}")

    except KeyboardInterrupt:
        print("\nCancelled")
    except Exception as e:
        print(f"Error getting stack info: {e}")
        raise click.Abort()


# Create the command object
info = click.command(name="info")(
    click.argument("stack_id", required=False)(click.pass_context(_info))
)
