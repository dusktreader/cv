from pathlib import Path
from typing import Annotated

import typer
from livereload import Server

from cv.schemas import CV


cli = typer.Typer()


@cli.callback(invoke_without_command=True)
def page(
    debug: Annotated[bool, typer.Option(help="Force a refresh every 3 seconds.")] = False,
):
    """
    Add to cv.html to enable livereload:
    <script src="http://localhost:5500/livereload.js?LR-verbose=true"></script>
    """

    def rebuild_json():
        print("Rebuilding cv.json...")
        cv: CV = CV.parse(Path("cv.yaml"))
        cv.dump(Path("static/cv.json"))
        print("Done!")

    rebuild_json()

    server: Server = Server()
    server.watch("static")
    server.watch("cv.yaml", func=rebuild_json)
    server.watch("cv.html")
    server.serve(default_filename="cv.html", open_url_delay=1)
