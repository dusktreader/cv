from pathlib import Path
from typing import Annotated
from xml.dom.minidom import Document, Element, parseString, Node

import typer
from buzz import require_condition
from loguru import logger
from markdown import markdown

from app.constants import ColorScheme


cli = typer.Typer()


@cli.callback(invoke_without_command=True)
def build(
    color: Annotated[ColorScheme, typer.Option(help="Render with color scheme.")] = ColorScheme.light,
):
    build_page(color)


def get_html_path() -> Path:
    return Path("index.html")


def build_page(color: ColorScheme) -> Path:
    logger.debug(f"Building PDF using scheme {color}")
    md_path = Path("README.md")

    html_content = markdown(md_path.read_text())
    html_content = fill_html(html_content, color)
    html_content = inject_divs(html_content)
    html_content = inject_photo(html_content)
    html_content = tag_emojis(html_content)

    html_path = get_html_path()
    logger.debug(f"Writing HTML file to {html_path}")
    html_path.write_text(html_content)

    return html_path


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


def _pretty_html(dom: Document) -> str:
    return "\n".join([l for l in dom.toprettyxml(indent="  ").split("\n") if l.strip()])


def find_element(parent: Document | Element, tag_name: str, class_name: str) -> Node:
    elements = []
    for node in parent.getElementsByTagName(tag_name):
        if node.getAttribute("class") == class_name:
            elements.append(node)
    require_condition(
        len(elements) == 1,
        f"Expected 1 element, found{len(elements)}",
        raise_exc_class=RuntimeError
    )
    return elements[0]


def fill_html(html: str, color: ColorScheme) -> str:
    logger.debug("Filling out HTML")
    html = f"""
        <html>
            <head>
                <meta charset="UTF-8" />
                <title>Tucker Beck Resumé</title>
                <link rel="stylesheet" href="css/styles.css" />
                <link rel="stylesheet" href="css/{color}.css" />
            </head>
            <body>
                {html}
            </body>
        </html>
    """
    dom = parseString(html)
    return _pretty_html(dom)


def inject_photo(html: str) -> str:
    logger.debug("Injecting photo into HTML")
    dom = parseString(html)
    header_div = find_element(dom, "div", "header")

    header_photo_div = dom.createElement("div")
    header_photo_div.setAttribute("class", "header-photo")
    header_div.insertBefore(header_photo_div, header_div.firstChild)
    header_photo_img = dom.createElement("img")
    header_photo_img.setAttribute("src", "images/me.png")
    header_photo_img.setAttribute("alt", "Tucker Beck Photo")
    header_photo_div.appendChild(header_photo_img)

    header_info_div = dom.createElement("div")
    header_info_div.setAttribute("class", "header-info")
    header_div.insertBefore(header_info_div, header_photo_div.nextSibling)
    _move_nodes_in_place(header_info_div.nextSibling, header_div.childNodes[-1], header_info_div)

    return _pretty_html(dom)


def inject_divs(html: str) -> str:
    logger.debug("Injecting divs into HTML")
    dom = parseString(html)

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

    contact_list_div = dom.createElement("div")
    contact_list_div.setAttribute("class", "contact_list")
    title_element = header_div.getElementsByTagName("h1")[0]
    header_div.insertBefore(contact_list_div, title_element.nextSibling)
    contact_list_element = header_div.getElementsByTagName("ul")[0]
    _move_nodes_in_place(contact_list_element, contact_list_element.nextSibling, contact_list_div)

    summary_div = dom.createElement("div")
    summary_div.setAttribute("class", "summary")
    summary_element = header_div.getElementsByTagName("p")[0]
    header_div.insertBefore(summary_div, summary_element)
    _move_nodes_in_place(summary_element, summary_element.nextSibling, summary_div)

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

    return _pretty_html(dom)


def tag_emojis(html: str) -> str:
    logger.debug("Marking emojis")

    dom = parseString(html)

    contact_list_div = find_element(dom, "div", "contact_list")
    li_elements = contact_list_div.getElementsByTagName("li")
    for li in li_elements:
        text_node = li.firstChild
        text_node.replaceWholeText(text_node.data.strip())
        p = dom.createElement("p")
        p.setAttribute("class", "emoji")
        li.insertBefore(p, text_node)
        _move_nodes_in_place(text_node, text_node.nextSibling, p)

        contact_div = dom.createElement("div")
        contact_div.setAttribute("class", "contact")
        li.insertBefore(contact_div, li.firstChild)
        _move_nodes_in_place(contact_div.nextSibling, li.childNodes[-1], contact_div)

    return _pretty_html(dom)
