from importlib.metadata import version as pkgVersion
import click

from .ui import TermTyper

@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option("--version", "-v", is_flag=True, help="Show version and exit.")
def main(version: bool):
    if(version):
        return print(f"termtyper - v{pkgVersion('termtyper')}")

    TermTyper().run()
