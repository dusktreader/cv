from pathlib import Path
from typing import Annotated

import typer
from livereload import Server, shell


cli = typer.Typer()


@cli.command()
def file(
    filename: Annotated[Path, typer.Option(help="The filename to watch.")] = Path("tucker-beck-cv--light.pdf"),
):
    server = Server()
    server.watch("README.md", shell("make light"))
    server.serve(default_filename=str(filename))
