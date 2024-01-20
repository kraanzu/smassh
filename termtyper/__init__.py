from importlib.metadata import version as pkgVersion
import click

from .ui import TermTyper
from termtyper.src.plugins.add_language import AddLanguage


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.option("--version", "-v", is_flag=True, help="Show version and exit.")
@click.pass_context
def main(ctx, version: bool):
    if version:
        return print(f"termtyper - v{pkgVersion('termtyper')}")

    if ctx.invoked_subcommand is None:
        TermTyper().run()


@main.command
@click.argument("name")
def add(name: str):
    AddLanguage().add(name)
