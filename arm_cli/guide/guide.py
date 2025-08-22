import click


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


@guide.command()
def chatbot():
    """Access ARM CLI chatbot"""
    print("Chatbot stub")