import os

import click

from arm_cli import __version__

# Skip expensive imports during completion
_COMPLETING = os.environ.get("_ARM_CLI_COMPLETE") or os.environ.get("COMP_WORDS")

if not _COMPLETING:
    from arm_cli.config import load_config
else:
    # Dummy config for completion
    def load_config():
        class DummyConfig:
            active_project = ""
            available_projects = []

        return DummyConfig()


class LazyGroup(click.Group):
    """A group that loads commands lazily"""

    def __init__(self, *args, lazy_subcommands=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Map of command name to import path
        self.lazy_subcommands = lazy_subcommands or {}

    def list_commands(self, ctx):
        return sorted(self.lazy_subcommands.keys())

    def get_command(self, ctx, cmd_name):
        if cmd_name in self.lazy_subcommands:
            module_path, attr_name = self.lazy_subcommands[cmd_name].rsplit(":", 1)
            mod = __import__(module_path, fromlist=[attr_name])
            return getattr(mod, attr_name)
        return None


@click.version_option(version=__version__)
@click.group(
    cls=LazyGroup,
    context_settings=dict(help_option_names=["-h", "--help"]),
    lazy_subcommands={
        "app": "arm_cli.app.app:app",
        "catalog": "arm_cli.catalog.catalog:catalog",
        "container": "arm_cli.container.container:container",
        "deploy": "arm_cli.deploy.deploy:deploy",
        "dev": "arm_cli.dev.dev:dev",
        "self": "arm_cli.self.self:self",
        "system": "arm_cli.system.system:system",
    },
)
@click.pass_context
def cli(ctx):
    """CLI for ARM Robotics framework - manage applications, catalogs, and deployments"""
    # Load config and store in context
    ctx.ensure_object(dict)
    ctx.obj["config"] = load_config()


if __name__ == "__main__":
    cli()
