import os
from pathlib import Path
from typing import Annotated

import typer
from livereload import Server
from loguru import logger
from weasyprint import html

from app.constants import ColorScheme
from app.resume import build_page, __file__ as resume_module_file, get_html_path


cli = typer.Typer()


@cli.callback(invoke_without_command=True)
def page(
    color: Annotated[ColorScheme, typer.Option(help="Render with color scheme.")] = ColorScheme.light,
):
    def _build():
       build_page(color)

    html_path = get_html_path()
    _build()
    server = Server()
    logger.debug(f"Adding README.md to watchers")
    readme_path = Path("README.md")
    server.watch(readme_path, func=_build)
    etc_path = Path("etc/css")
    for css_path in etc_path.glob("*.css"):
        logger.debug(f"Adding {css_path} to watchers")
        server.watch(str(css_path), func=_build)
    logger.debug(f"Adding {resume_module_file} to watchers")
    server.watch(resume_module_file, func=_build)

    server.serve(default_filename=str(html_path), open_url_delay=0.25, live_css=False)
