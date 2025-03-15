from pathlib import Path
from xml.dom.minidom import Document, Element, parseString, Node

import typer
from loguru import logger
from markdown import markdown

from app.constants import DEFAULT_COLOR, ColorScheme, DEFAULT_SIZE, Size


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
    html_content = add_download_button(html_content)
    html_content = add_color_switcher(html_content)
    html_content = add_size_switcher(html_content)
    html_content = add_switcher_script(html_content)
    if debug:
        html_content = inject_auto_refresh(html_content)

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


def find_element(parent: Document | Element, tag_name: str, class_name: str | None = None) -> Node:
    elements = []
    for node in parent.getElementsByTagName(tag_name):
        if class_name:
            if node.getAttribute("class") == class_name:
                elements.append(node)
        else:
            elements.append(node)
    if len(elements) != 1:
        raise RuntimeError(f"Expected 1 element, found{len(elements)}")
    return elements[0]


def find_id(root: Node | Document | Element, id_name: str) -> Node | None:
    if isinstance(root, Element) and root.getAttribute("id") == id_name:
        return root
    for node in root.childNodes:
        descendant = find_id(node, id_name)
        if descendant is not None:
            return descendant
    return None


def add_css_link(dom: Document, parent: Element, name: str, html_id: str | None = None) -> None:
    css = dom.createElement("link")
    css.setAttribute("rel", "stylesheet")
    css.setAttribute("type", "text/css")
    css.setAttribute("href", f"static/css/{name}.css")
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
    add_css_link(dom, head, DEFAULT_SIZE, "size-style")
    add_css_link(dom, head, DEFAULT_COLOR, "color-style")

    body = dom.createElement("body")
    html_node.appendChild(body)

    markdown_fragment = parseString(f"<xxx>{html}</xxx>")
    for child in markdown_fragment.documentElement.childNodes:
        imported_node = dom.importNode(child, deep=True)
        body.appendChild(imported_node)

    return _pretty_html(dom)


def inject_photo(html: str) -> str:
    logger.debug("Injecting photo into HTML")
    dom = parseString(html)
    header_div = find_element(dom, "div", class_name="header")

    header_photo_div = dom.createElement("div")
    header_photo_div.setAttribute("class", "header-photo")
    header_div.insertBefore(header_photo_div, header_div.firstChild)
    header_photo_img = dom.createElement("img")
    header_photo_img.setAttribute("src", "static/images/me.png")
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

    switcher_div = dom.createElement("div")
    switcher_div.setAttribute("id", "switchers")
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

    contact_list_div = find_element(dom, "div", class_name="contact_list")
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


def add_download_button(html: str) -> str:
    logger.debug("Adding download/print button")

    dom = parseString(html)

    switcher_menus = find_id(dom, "switcher-menus")
    assert switcher_menus is not None

    switcher_list = find_id(dom, "switcher-list")
    assert switcher_list is not None

    menu_button = dom.createElement("button")
    menu_button.setAttribute("id", "download-menu")
    menu_button.setAttribute("class", "switcher-menu no-print")
    menu_button.appendChild(dom.createTextNode("🖨"))
    switcher_menus.appendChild(menu_button)

    button_container = dom.createElement("div")
    button_container.setAttribute("class", "switcher-buttons")
    button_container.setAttribute("id", "download-buttons")
    switcher_list.appendChild(button_container)

    download_button = dom.createElement("button")
    download_button.setAttribute("class", f"switcher-button download-button no-print")
    download_button.setAttribute("onclick", "window.print()")
    download_span = dom.createElement("span")
    download_span.appendChild(dom.createTextNode("Download/Print"))
    download_button.appendChild(download_span)
    button_container.appendChild(download_button)

    return _pretty_html(dom)


def add_color_switcher(html: str) -> str:
    logger.debug("Adding color switcher")

    dom = parseString(html)

    switcher_menus = find_id(dom, "switcher-menus")
    assert switcher_menus is not None

    switcher_list = find_id(dom, "switcher-list")
    assert switcher_list is not None

    menu_button = dom.createElement("button")
    menu_button.setAttribute("id", "color-menu")
    menu_button.setAttribute("class", "switcher-menu no-print")
    menu_button.appendChild(dom.createTextNode("🔅"))
    switcher_menus.appendChild(menu_button)

    button_container = dom.createElement("div")
    button_container.setAttribute("class", "switcher-buttons")
    button_container.setAttribute("id", "color-buttons")
    switcher_list.appendChild(button_container)

    for color in ColorScheme:
        color_button = dom.createElement("button")
        color_button.setAttribute("class", f"switcher-button color-button no-print")
        color_button.setAttribute("onclick", f"changeColor('{color}')")
        color_span = dom.createElement("span")
        color_span.setAttribute("class", f"color-sigil-{color}")
        color_span.appendChild(dom.createTextNode(color))
        color_button.appendChild(color_span)
        button_container.appendChild(color_button)

    return _pretty_html(dom)


def add_size_switcher(html: str) -> str:
    logger.debug("Adding size switcher")

    dom = parseString(html)

    switcher_menus = find_id(dom, "switcher-menus")
    assert switcher_menus is not None

    switcher_list = find_id(dom, "switcher-list")
    assert switcher_list is not None

    menu_button = dom.createElement("button")
    menu_button.setAttribute("id", "size-menu")
    menu_button.setAttribute("class", "switcher-menu no-print")
    menu_button.appendChild(dom.createTextNode("🔍"))
    switcher_menus.appendChild(menu_button)

    button_container = dom.createElement("div")
    button_container.setAttribute("class", "switcher-buttons")
    button_container.setAttribute("id", "size-buttons")
    switcher_list.appendChild(button_container)

    for size in Size:
        size_button = dom.createElement("button")
        size_button.setAttribute("class", f"size-button switcher-button no-print")
        size_button.setAttribute("onclick", f"changeSize('{size}')")
        size_span = dom.createElement("span")
        size_span.setAttribute("class", f"size-sigil-{size}")
        size_span.appendChild(dom.createTextNode(size))
        size_button.appendChild(size_span)
        button_container.appendChild(size_button)

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
