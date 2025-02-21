from pathlib import Path
from typing import Annotated

import typer
from auto_name_enum import AutoNameEnum, auto
from markdown import markdown
from weasyprint import HTML


app = typer.Typer(rich_markup_mode="rich")


class ColorScheme(AutoNameEnum):
    light = auto()
    night = auto()
    sizzle = auto()


@app.command()
def render(
    color: Annotated[ColorScheme, typer.Option(help="Render with color scheme.")] = ColorScheme.light,
    prefix: Annotated[str, typer.Option(help="The prefix for generated filenames.")] = "tucker-beck-cv",
):
    md_path = Path("README.md")
    html_content = markdown(md_path.read_text())
    css_paths = [Path("etc/styles.css"), Path(f"etc/{color}.css")]
    filename = f"{prefix}--{color}.pdf"
    html = HTML(string=html_content)
    html.write_pdf(filename, stylesheets=css_paths)


if __name__ == "__main__":
    app()
