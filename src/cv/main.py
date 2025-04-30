from typing import Annotated

import typer

from cv.version import show_version
from cv.build import cli as build_cli
from cv.watch import cli as watch_cli


cli = typer.Typer(rich_markup_mode="rich")


@cli.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Annotated[bool, typer.Option(help="Print the version of and exit")] = False,
):
    if version:
        show_version()
        ctx.exit()

    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        ctx.exit()


cli.add_typer(build_cli, name="build")
cli.add_typer(watch_cli, name="watch")


if __name__ == "__main__":
    cli()
