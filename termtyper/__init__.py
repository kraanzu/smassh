from importlib.metadata import version as getVersion
import click

from .ui import TermTyper

@click.command
@click.option("--version", "-v", is_flag=True, help="Show version", default=False)
def main(version):
    if(version):
        ver = getVersion("termtyper")
        print(f"termtyper - {ver}")
        return

    TermTyper().run()
