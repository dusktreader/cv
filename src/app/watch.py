import base64
from pathlib import Path
from typing import Annotated

import typer
from livereload import Server
from loguru import logger

from app.constants import ColorScheme
from app.resume import build_pdf, __file__ as resume_module_file


cli = typer.Typer()


@cli.callback(invoke_without_command=True)
def pdf(
    color: Annotated[ColorScheme, typer.Option(help="Render with color scheme.")] = ColorScheme.light,
    dump_html: Annotated[bool, typer.Option(help="Dump HTML file.")] = False,
):
    def _build():
        pdf_path = build_pdf(color, "tucker-beck-cv", dump_html)
        encoded = base64.b64encode(pdf_path.read_bytes()).decode('utf-8')
        Path(".watch.html").write_text(
            f"""
                <html>
                    <head>
                    </head>
                    <body>
                        <embed src="data:application/pdf;base64,{encoded}"
                               type="application/pdf"
                               width="100%"
                               height="100%"
                        >
                    </body>
                </html>
            """
        )

    _build()
    server = Server()
    logger.debug(f"Adding README.md to watchers")
    server.watch("README.md", func=_build)
    for etc_path in Path("etc/css").glob("*.css"):
        logger.debug(f"Adding {etc_path} to watchers")
        server.watch(str(etc_path), func=_build)
    logger.debug(f"Adding {resume_module_file} to watchers")
    server.watch(resume_module_file, func=_build)

    server.serve(default_filename=".watch.html", open_url_delay=0.25, live_css=False)
