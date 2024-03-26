import click

PKG_VERSION = "3.1.3"


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.option(
    "--version",
    "-v",
    is_flag=True,
    help="Show version and exit.",
)
@click.pass_context
def main(ctx, version: bool) -> None:
    if version:
        return print(f"smassh - v{PKG_VERSION}")

    if ctx.invoked_subcommand is None:
        from smassh.ui.tui import Smassh

        Smassh().run()


@main.command(help="Add a language to smassh")
@click.argument("name")
def add(name: str) -> None:
    from smassh.src.plugins.add_language import AddLanguage

    AddLanguage().add(name)


if __name__ == "__main__":
    main()
