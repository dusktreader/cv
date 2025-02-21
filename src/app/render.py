from pathlib import Path
from typing import Annotated
from xml.dom.minidom import parseString, Document, Node

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
    dump_html: Annotated[bool, typer.Option(help="Dump HTML file.")] = False,
):
    md_path = Path("README.md")

    name = f"{prefix}--{color}"
    pdf_path = Path(f"{name}.pdf")

    html_content = markdown(md_path.read_text())
    html_content = injectDivs(html_content)

    if dump_html:
        html_path = Path(f"{name}.html")
        html_path.write_text(html_content)

    css_paths = [Path("etc/styles.css"), Path(f"etc/{color}.css")]
    html = HTML(string=html_content)
    html.write_pdf(pdf_path, stylesheets=css_paths)


def _move_nodes_in_place(
    start_node: Node,
    end_node: Node | None,
    target_node: Node,
) -> None:
    nodes_to_move = []
    current_node = start_node
    while current_node and current_node != end_node:
        nodes_to_move.append(current_node)
        current_node = current_node.nextSibling
    for node in nodes_to_move:
        target_node.appendChild(node)


def injectDivs(html: str) -> str:
    doc = f"""
        <html>
            <head>
                <title>Tucker Beck CV</title>
            </head>
            <body>
                {html}
            </body>
        </html>
    """
    dom = parseString(doc)

    body = dom.getElementsByTagName("body")[0]

    container_div = dom.createElement("div")
    container_div.setAttribute("class", "container")
    body.insertBefore(container_div, body.firstChild)
    anchor = container_div.nextSibling
    assert anchor is not None
    _move_nodes_in_place(anchor, None, container_div)

    header_div = dom.createElement("div")
    header_div.setAttribute("class", "header")
    container_div.insertBefore(header_div, container_div.firstChild)
    h2_elements = container_div.getElementsByTagName("h2")
    sidebar_start = next(e for e in h2_elements if e.firstChild.data == "Skills")
    _move_nodes_in_place(header_div.nextSibling, sidebar_start, header_div)

    bottom_div = dom.createElement("div")
    bottom_div.setAttribute("class", "bottom")
    container_div.insertBefore(bottom_div, header_div.nextSibling)
    _move_nodes_in_place(bottom_div.nextSibling, None, bottom_div)

    sidebar_div = dom.createElement("div")
    sidebar_div.setAttribute("class", "sidebar")
    bottom_div.insertBefore(sidebar_div, bottom_div.firstChild)
    h2_elements = bottom_div.getElementsByTagName("h2")
    main_start = next(e for e in h2_elements if e.firstChild.data == "Experience")
    _move_nodes_in_place(sidebar_div.nextSibling, main_start, sidebar_div)

    main_div = dom.createElement("div")
    main_div.setAttribute("class", "main")
    bottom_div.insertBefore(main_div, sidebar_div.nextSibling)
    _move_nodes_in_place(main_start, None, main_div)

    return dom.toprettyxml(indent="  ")


if __name__ == "__main__":
    app()
