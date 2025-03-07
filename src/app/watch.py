import subprocess
from pathlib import Path
from typing import Annotated

import typer
from loguru import logger
from watchfiles import run_process

from app.constants import ColorScheme
from app.build import build, build_page, __file__ as build_module_file, get_html_path


cli = typer.Typer()


@cli.callback(invoke_without_command=True)
def page(
    color: Annotated[ColorScheme, typer.Option(help="Render with color scheme.")] = ColorScheme.light,
):
    html_path = get_html_path()
    static_path = Path("static")
    readme_path = Path("README.md")

    watch_paths = [build_module_file, html_path, static_path, readme_path]

    logger.debug("Triggering initial build")
    build_page(color, debug=True)

    logger.debug("Opening browser to page")
    subprocess.run(["explorer.exe", str(html_path)])

    logger.debug(f"Watching for changes in {watch_paths}")
    run_process(*watch_paths, target=build_page, args=(color,), kwargs=dict(debug=True))
