from pathlib import Path
from typing import Annotated

import typer

from cv.schemas import CV
from cv.markdown import build as markdown_build


cli = typer.Typer()


@cli.command()
def markdown(target: Annotated[Path | None, typer.Option(help="Target path to build")] = None):
    if target is None:
        target = Path("README.md")
    cv: CV = CV.parse(Path("cv.yaml"))
    text = markdown_build(cv)
    target.write_text(text)


@cli.command()
def json(
    yaml_path: Annotated[Path | None, typer.Option(help="Path to the source CV YAML file")] = None,
    json_path: Annotated[Path | None, typer.Option(help="Path to the target CV JSON file")] = None,
):
    if not yaml_path:
        yaml_path = Path("cv.yaml")
    if not json_path:
        json_path = Path("static/cv.json")
    cv: CV = CV.parse(Path("cv.yaml"))
    cv.dump(json_path)
