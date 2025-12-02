import click

from arm_cli.guide.chatbot import chatbot


@click.group()
def guide():
    """Guide and help resources for ARM CLI"""
    pass


@guide.command()
def cheatsheet():
    """Show ARM CLI cheatsheet"""
    print("Cheatsheet stub")


@guide.command()
def documentation():
    """Show ARM CLI documentation"""
    print("Documentation stub")


# Add chatbot subcommands
guide.add_command(chatbot)