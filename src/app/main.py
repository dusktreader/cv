import typer

from app.version import show_version
from app.logging import init_logs
from app.build import cli as build_cli
from app.watch import cli as watch_cli


cli = typer.Typer(rich_markup_mode="rich")


@cli.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, help="Enable verbose logging to the terminal"),
    version: bool = typer.Option(False, help="Print the version of and exit"),
):
    if version:
        show_version()
        ctx.exit()

    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        ctx.exit()

    init_logs(verbose=verbose)


cli.add_typer(build_cli, name="build")
cli.add_typer(watch_cli, name="watch")


if __name__ == "__main__":
    cli()
