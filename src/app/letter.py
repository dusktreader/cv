import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Annotated, Any

import httpx
import snick
import typer
from buzz import enforce_defined, handle_errors
from inflection import parameterize
from loguru import logger
from markdown import markdown
from openai import OpenAI
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from weasyprint import HTML

from app.config import settings
from app.main import cli


def generate_letter(
    posting_text: str,
    resume_text: str,
    example_text: str | None = None,
    reprompts: list[tuple[str, str]] | None = None,
    fake: bool = False,
) -> str:

    api_key: str = enforce_defined(
        settings.OPENAI_API_KEY,
        message="You must have OPENAI_API_KEY configured (env or .env)!",
        raise_exc_class=ValueError,
    )
    client = OpenAI(api_key=api_key)

    prompt = f"""
        You are a professional resume writer and career coach. Your task is to generate
        a cover letter for a job application based on the provided job posting and
        resume. You will be given a job posting and a resume, and you need to create a
        tailored cover letter that highlights the candidate's qualifications and
        suitability for the position.

        The job posting that follows is html scraped from a job board. It will contain
        a lot of markup, but you should ignore it and focus on the text content.

        {posting_text}

        You should use the following resume as a reference. It is a markdown document.

        {resume_text}
    """
    if example_text:
        prompt += f"""
            You should use this cover letter as reference for what I would like the
            resulting cover letter to look like. It is a markdown document.

            {example_text}
        """

    prompt += f"""
        The cover letter should not sound like it was written by a machine. It should
        be direct, personal, and energetic. It should be professional, but informal
        in an almost daring way.

        Avoid sentences of the form, "With X, I will Y". Do not use any of the following
        words:

        - challenge
        - opportunity
        - leverage
        - passionate

        The letter should highlight my leadership, my technical excellence, and my
        ambition.

        Use the salutation, "To the Hiring Team at <company name>", where <company name>
        is the name of the company found in the job posting.

        Use the following markdown for the closing exactly as it appears:

            Best regards,

            ![signature](file://{Path("etc/sig.png").absolute()})

            Tucker Beck

        The final letter should be in markdown format. Do not include any other text.
        Just print the letter itself.

        Again, do not provide any friendly text before the letter. Do not explain what
        you are doing. Do not say "Here is your letter". Just print the damn letter.

        Use this for the markdown heading exactly as it is:

            # Tucker Beck

            📍 [Camas, WA](https://goo.gl/maps/zgVAgxrRwfM1EPpf9) /
            📧 [Tucker.beck@gmail.com](tucker.beck@gmail.com) /
            🛠 [dusktreader@github](https://github.com/dusktreader)

            ---
    """

    messages=[
        dict(role="developer", content=prompt),
        dict(role="user", content="Please write me a nice letter!"),
    ]

    if reprompts is not None:
        for (old_letter, user_feedback) in reprompts:
            messages.append(dict(role="assistant", content=old_letter))
            messages.append(dict(role="user", content=user_feedback))

    kwargs = dict(
        model="gpt-4o",
        n=1,
        messages=messages,
    )
    logger.debug(f"Getting openai output using params: \n{json.dumps(kwargs, indent=2)}")
    if fake:
        text = snick.dedent(f"""
            # Tucker Beck

            📍 [Camas, WA](https://goo.gl/maps/zgVAgxrRwfM1EPpf9) /
            📧 [Tucker.beck@gmail.com](tucker.beck@gmail.com) /
            🛠 [dusktreader@github](https://github.com/dusktreader)

            ---
            Dear FAKE:

            I am cool!

            Sincerely,

            ![signature](file://{Path("etc/sig.png").absolute()})

            Tucker Beck
        """)
    else:
        cmp = client.chat.completions.create(**kwargs)  # type: ignore
        text = cmp.choices[0].message.content
        assert text is not None
    return text


@cli.command()
def letter(
    posting_url: Annotated[str, typer.Argument(help="The URL of the job posting.")],
    company: Annotated[str | None, typer.Option(help="The name of the company.")] = None,
    position: Annotated[str | None, typer.Option(help="The title for the job.")] = None,
    example_letter: Annotated[Path | None, typer.Option(help="An example letter to use as a reference.")] = None,
    prefix: Annotated[str, typer.Option(help="The prefix for generated filenames.")] = "cover-letter",
    dump_html: Annotated[bool, typer.Option(help="Dump HTML file.")] = False,
    fake: Annotated[bool, typer.Option(help="Don't call OpenAI. Use a fake letter.")] = False,
):
    with handle_errors(
        "Failed to generate cover letter",
        raise_exc_class=typer.Exit,
        raise_kwargs=dict(code=1),
        do_except=lambda dep: print(f"[red]{dep.final_message}[/red]"),
        exc_builder=lambda ebp: ebp.raise_exc_class(*ebp.raise_args, **ebp.raise_kwargs),
    ):
        resume_path = Path("README.md")
        logger.debug(f"Loading resume from {resume_path}")
        resume_text = resume_path.read_text()

        logger.debug(f"Pulling posting from {posting_url}")
        response = httpx.get(posting_url)
        response.raise_for_status()
        posting_text = response.text

        kwargs: dict[str, Any] = dict(fake=fake)
        if example_letter:
            logger.debug(f"Loading example letter from {example_letter}")
            kwargs["example_text"] = example_letter.read_text()

        logger.debug("Generating letter")

        text = generate_letter(posting_text, resume_text, **kwargs)

        accepted = False
        reprompts = []

        console = Console()

        while not accepted:
            console.print()
            console.print("Here is your generated letter:")
            console.print()
            console.print(Panel(Markdown(text), title="Generated Letter"))

            accepted = typer.confirm("Are you satisfied with the letter?", default=True)

            if not accepted:
                reprompts.append(
                    (
                        text,
                        typer.prompt(
                            "What can I do to fix it?",
                            default="Just try again"
                        ),
                    )
                )
                kwargs["reprompts"] = reprompts
                logger.debug("Regenerating letter based on feedback")
                text = generate_letter(posting_text, resume_text, **kwargs)

        edit = typer.confirm("Would you like to edit the letter?", default=False)
        if edit:
            logger.debug("Editing generated letter")
            with tempfile.NamedTemporaryFile() as tmp_file:
                tmp_path = Path(tmp_file.name)
                tmp_path.write_text(text)
                subprocess.run([os.environ["EDITOR"], str(tmp_path)])
                text = tmp_path.read_text()

        logger.debug("Saving letter to file")
        name = prefix
        if company:
            name += f"--{parameterize(company)}"
        if position:
            name += f"--{parameterize(position)}"
        pdf_path = Path(f"{name}.pdf")

        html_content = markdown(text)

        if dump_html:
            html_path = Path(f"{name}.html")
            logger.debug(f"Dumping html to {html_path}")
            html_path.write_text(html_content)

        css_paths = [Path("etc/css/letter/styles.css")]
        html = HTML(string=html_content)
        html.write_pdf(pdf_path, stylesheets=css_paths)
        console.print(f"Cover letter saved to {pdf_path}")
