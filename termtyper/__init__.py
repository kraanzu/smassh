from importlib.metadata import version
import click

from .ui import TermTyper

@click.command
@click.version_option(version("termtyper"), prog_name="termtyper")
def main():
    TermTyper().run()
