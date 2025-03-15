import subprocess
from pathlib import Path
from typing import Annotated

import typer
from loguru import logger
from watchfiles import run_process

from app.build import build_page, __file__ as build_module_file, get_html_path


cli = typer.Typer()


@cli.callback(invoke_without_command=True)
def page(
    auto_refresh: Annotated[bool, typer.Option(help="Force a refresh every 3 seconds.")] = False,
):
    html_path = get_html_path()
    static_path = Path("static")
    readme_path = Path("README.md")

    watch_paths = [build_module_file, html_path, static_path, readme_path]

    logger.debug("Triggering initial build")
    build_page(debug=True)

    logger.debug("Opening browser to page")
    subprocess.run(["explorer.exe", str(html_path)])

    logger.debug(f"Watching for changes in {watch_paths}")
    run_process(*watch_paths, target=build_page, kwargs=dict(debug=auto_refresh))
