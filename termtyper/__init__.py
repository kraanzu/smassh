import importlib.metadata
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
    args.add_argument(
        "-q",
        "--quiet",
        help="Run termtyper in quiet mode",
        action="store_true",
    )

    args = args.parse_args()

    if args.version:
        ver = importlib.metadata.version("termtyper")
        print(f"termtyper - {ver}")
        return

    TermTyper.run(args.quiet)
