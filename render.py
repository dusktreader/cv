from pathlib import Path
from typing import Annotated

import typer
from auto_name_enum import AutoNameEnum, auto
from markdown import markdown
from weasyprint import HTML


app = typer.Typer(rich_markup_mode="rich")


@app.command()
def render(dark: Annotated[bool, typer.Option(help="Render in dark mode.")] = False):
    md_path = Path("README.md")
    html_content = markdown(md_path.read_text())
    css_paths = [Path("etc/styles.css")]

    if dark:
        css_paths.append(Path("etc/dark.css"))
    else:
        css_paths.append(Path("etc/light.css"))

    HTML(string=html_content).write_pdf("tucker-beck-cv.pdf", stylesheets=css_paths)


if __name__ == "__main__":
    app()
