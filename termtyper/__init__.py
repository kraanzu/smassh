from importlib.metadata import version
import argparse

from .ui import TermTyper


def main():
    args = argparse.ArgumentParser()
    args.add_argument(
        "-v",
        "--version",
        help="Show version",
        action="store_true",
    )

    args = args.parse_args()

    if args.version:
        ver = version("termtyper")
        print(f"termtyper - {ver}")
        return

    TermTyper().run()
