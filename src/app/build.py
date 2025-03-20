from pathlib import Path
from xml.dom.minidom import Document, Element, parseString, Node

import typer
from buzz import require_condition, enforce_defined
from loguru import logger
from markdown import markdown

from app.constants import (
    ColorScheme,
    HtmlChoices,
    Size,
    Position,
    RenderAction,
)


cli = typer.Typer()


@cli.callback(invoke_without_command=True)
def build():
    build_page()


def get_html_path() -> Path:
    return Path("index.html")


def build_page(debug: bool = False) -> Path:
    logger.debug("Building html page")
    md_path = Path("README.md")

    html_content = markdown(md_path.read_text())
    html_content = fill_html(html_content)
    html_content = inject_divs(html_content)
    html_content = inject_photo(html_content)
    html_content = tag_emojis(html_content)
    html_content = add_switcher(html_content, RenderAction, override_map={RenderAction.download: "Print/Download"})
    html_content = add_switcher(html_content, Position)
    html_content = add_switcher(html_content, ColorScheme)
    html_content = add_switcher(html_content, Size)
    html_content = add_switcher_script(html_content)
    if debug:
        html_content = inject_auto_refresh(html_content)

    html_path = get_html_path()
    logger.debug(f"Writing HTML file to {html_path}")
    html_path.write_text(html_content)

    return html_path


def _pretty_html(dom: Document) -> str:
    return "\n".join([l for l in dom.toprettyxml(indent="  ").split("\n") if l.strip()])


def find_element(parent: Document | Element, tag_name: str) -> Node:
    elements = parent.getElementsByTagName(tag_name)
    require_condition(
        len(elements) == 1,
        f"Expected 1 element, found{len(elements)}",
        raise_exc_class=RuntimeError
    )
    return elements[0]


def find_id(root: Node | Document | Element, id_name: str) -> Node:

    def _fr(root: Node | Document | Element, id_name: str) -> Node | None:
        if isinstance(root, Element) and root.getAttribute("id") == id_name:
            return root
        for node in root.childNodes:
            descendant = _fr(node, id_name)
            if descendant is not None:
                return descendant
        return None

    return enforce_defined(
        _fr(root, id_name),
        "Couldn't find id",
        raise_exc_class=RuntimeError,
    )


def add_css_link(
    dom: Document,
    parent: Element,
    name: str,
    html_id: str | None = None,
    subdir: str | None = None,
) -> None:
    css_path = Path("static/css")
    if subdir:
        css_path = css_path / subdir
    css_path = css_path / f"{name}.css"

    css = dom.createElement("link")
    css.setAttribute("rel", "stylesheet")
    css.setAttribute("type", "text/css")
    css.setAttribute("href", str(css_path))
    if html_id:
        css.setAttribute("id", html_id)
    parent.appendChild(css)


def fill_html(html: str) -> str:
    logger.debug("Filling out HTML")

    dom = Document()
    html_node = dom.createElement("html")
    dom.appendChild(html_node)

    head = dom.createElement("head")
    html_node.appendChild(head)

    meta = dom.createElement("meta")
    meta.setAttribute("charset", "utf-8")
    head.appendChild(meta)

    title = dom.createElement("title")
    title.appendChild(dom.createTextNode("Tucker Beck Resumé"))
    head.appendChild(title)

    add_css_link(dom, head, "styles")
    add_css_link(dom, head, Size.default(), "size-style", subdir="sizes")
    add_css_link(dom, head, ColorScheme.default(), "color-style", subdir="colors")

    body = dom.createElement("body")
    html_node.appendChild(body)

    markdown_fragment = parseString(f"<xxx>{html}</xxx>")
    for child in markdown_fragment.documentElement.childNodes:
        imported_node = dom.importNode(child, deep=True)
        body.appendChild(imported_node)

    return _pretty_html(dom)


def _move_node(
    target_node: Node,
    to_parent: Node,
) -> None:
    from_parent = target_node.parentNode
    from_parent.removeChild(target_node)
    to_parent.appendChild(target_node)


def _move_nodes_range(
    start_node: Node,
    end_node: Node | None,
    to_parent: Node,
) -> None:
    current_node = start_node
    while current_node and current_node != end_node:
        next_node = current_node.nextSibling
        _move_node(current_node, to_parent)
        current_node = next_node


def inject_photo(html: str) -> str:
    logger.debug("Injecting photo into HTML")
    dom = parseString(html)

    header_photo_div = find_id(dom, "header-photo")

    header_photo_img = dom.createElement("img")
    header_photo_img.setAttribute("src", "static/images/me.png")
    header_photo_img.setAttribute("alt", "Tucker Beck Photo")
    header_photo_div.appendChild(header_photo_img)

    return _pretty_html(dom)


def _make_div(
    dom: Document,
    parent_node: Node | None = None,
    element_id: str | None = None,
    class_name: str | None = None,
) -> Node:
    div = dom.createElement("div")
    if element_id:
        div.setAttribute("id", element_id)
    if class_name:
        div.setAttribute("class", class_name)
    if parent_node:
        parent_node.appendChild(div)
    return div


def inject_divs(html: str) -> str:
    logger.debug("Injecting divs into HTML")
    dom = parseString(html)

    body = dom.getElementsByTagName("body")[0]

    # Create container
    container_div = _make_div(dom, element_id="container")
    body.insertBefore(container_div, body.firstChild)

    # Add principle divs
    header_div = _make_div(dom, parent_node=container_div, element_id="header")
    bottom_div = _make_div(dom, parent_node=container_div, element_id="bottom")

    # Add bottom divs
    sidebar_div = _make_div(dom, parent_node=bottom_div, element_id="sidebar")
    main_div = _make_div(dom, parent_node=bottom_div, element_id="main")

    # Add header sub-divs
    header_photo_div = _make_div(dom, parent_node=header_div, element_id="header-photo")
    header_info_div = _make_div(dom, parent_node=header_div, element_id="header-info")

    # Add header-info sub-divs
    title_div = _make_div(dom, parent_node=header_info_div, element_id="title")
    title_x_div = _make_div(dom, parent_node=title_div, element_id="title-x")
    contact_list_div = _make_div(dom, parent_node=header_info_div, element_id="contact-list")
    summary_div = _make_div(dom, parent_node=header_info_div, element_id="summary")

    # Identify title elements
    name_element = body.getElementsByTagName("h1")[0]
    name_element.setAttribute("id", "title-name")

    h2_elements = body.getElementsByTagName("h2")

    position_element = h2_elements[0]
    position_element.setAttribute("id", "title-position")

    # Identify contact element
    contact_list_element = body.getElementsByTagName("ul")[0]
    summary_element = body.getElementsByTagName("p")[0]

    # Identify sidebar elements
    sidebar_start = h2_elements[1]
    main_start = next(e for e in h2_elements if e.firstChild.data == "Experience")

    # Move header title elements
    _move_node(name_element, title_x_div)
    _move_node(position_element, title_x_div)
    _move_node(contact_list_element, contact_list_div)
    _move_node(summary_element, summary_div)

    # Move sidebar elements
    _move_nodes_range(sidebar_start, main_start, sidebar_div)

    # Move main elements
    _move_nodes_range(main_start, None, main_div)

    # Add switchers
    switcher_div = dom.createElement("div")
    switcher_div.setAttribute("id", "switchers")
    switcher_div.setAttribute("class", "no-print")
    body.appendChild(switcher_div)

    switcher_menus = dom.createElement("div")
    switcher_menus.setAttribute("id", "switcher-menus")
    switcher_div.appendChild(switcher_menus)

    switcher_list = dom.createElement("div")
    switcher_list.setAttribute("id", "switcher-list")
    switcher_div.appendChild(switcher_list)

    return _pretty_html(dom)


def tag_emojis(html: str) -> str:
    logger.debug("Marking emojis")

    dom = parseString(html)

    contact_list_div = find_id(dom, "contact-list")
    li_elements = contact_list_div.getElementsByTagName("li")
    for li in li_elements:
        contact_div = dom.createElement("div")
        contact_div.setAttribute("class", "contact")
        li.insertBefore(contact_div, li.firstChild)

        text_node = contact_div.nextSibling
        text_node.replaceWholeText(text_node.data.strip())

        p = dom.createElement("p")
        p.setAttribute("class", "emoji")

        a = text_node.nextSibling
        a.setAttribute("class", "contact-link")

        _move_node(text_node, p)
        contact_div.appendChild(p)
        _move_node(a, contact_div)

    return _pretty_html(dom)


def add_switcher(
    html: str,
    options: type[HtmlChoices],
    override_map: dict[HtmlChoices, str] | None = None,
) -> str:
    label = options.label()
    emoji = options.class_emoji()
    if override_map is None:
        override_map = {}

    logger.debug(f"Adding {label} switcher")

    dom = parseString(html)

    switcher_menus = find_id(dom, "switcher-menus")
    switcher_list = find_id(dom, "switcher-list")

    menu_button = dom.createElement("button")
    menu_button.setAttribute("id", f"{label}-menu")
    menu_button.setAttribute("class", "switcher-menu")
    menu_button.appendChild(dom.createTextNode(emoji))
    switcher_menus.appendChild(menu_button)

    button_container = dom.createElement("div")
    button_container.setAttribute("class", "switcher-buttons")
    button_container.setAttribute("id", f"{label}-buttons")
    switcher_list.appendChild(button_container)

    for option in options:
        option_button = dom.createElement("button")
        option_button.setAttribute("class", f"switcher-button {label}-button")
        option_button.setAttribute("onclick", option.js())
        button_container.appendChild(option_button)

        option_button_div = dom.createElement("div")
        option_button_div.setAttribute("class", f"button-internals")
        option_button.appendChild(option_button_div)

        option_emoji = dom.createElement("span")
        option_emoji.setAttribute("class", f"switcher-button-emoji")
        option_emoji.setAttribute("id", f"{label}-{option}-switcher-button-emoji")
        option_emoji.appendChild(dom.createTextNode(option.emoji()))
        option_button_div.appendChild(option_emoji)

        option_text = dom.createElement("span")
        option_text.setAttribute("class", f"switcher-button-text")
        option_text.setAttribute("id", f"{label}-{option}-switcher-button-text")
        option_text.appendChild(dom.createTextNode(
            override_map.get(option, option.capitalize())
        ))
        option_button_div.appendChild(option_text)

    return _pretty_html(dom)


def add_switcher_script(html: str) -> str:
    logger.debug("Adding switcher script")

    dom = parseString(html)
    body = find_element(dom, "body")

    script = dom.createElement("script")
    script.setAttribute("src", "static/js/switchers.js")

    # This is so fucking stupid
    script.appendChild(dom.createTextNode(" "))
    body.appendChild(script)

    return _pretty_html(dom)


def inject_auto_refresh(html: str) -> str:
    logger.debug("Adding live reload script")

    dom = parseString(html)

    head = find_element(dom, "head")
    meta = dom.createElement("meta")
    meta.setAttribute("http-equiv", "refresh")
    meta.setAttribute("content", "3")
    head.appendChild(meta)

    return _pretty_html(dom)
