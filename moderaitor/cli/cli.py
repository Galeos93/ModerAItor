# Monolithic app

# Insert url
## Scrape and format post
# Fed posts to app
from itertools import islice
import os
import typing

import typer

from moderaitor import database_utils
from moderaitor import scrapper
from moderaitor import models
from moderaitor.llm.openassistant import get_model as get_openassistant_model
from moderaitor.cli import __app_name__, __version__

COMMENTS_BUCKET = os.getenv("COMMENTS_BUCKET", "quarantined-comments")

app = typer.Typer()

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.command()
def main(
    version: typing.Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
    url: str = typer.Argument(
        help="URL that contains comments to moderate.",
    ),
    rules: str = typer.Argument(
        help="Rules used as a base for the moderation.",
    ),
    with_context: typing.Optional[bool] = typer.Option(
        None,
        "--with-context",
        help="Return context about the decision taken after moderation."
    ),
    max_items: typing.Optional[int] = typer.Option(
        None,
        "--max-items",
        help="Maximum of items to moderate."
    )
) -> None:
    generator = scrapper.generator_factory(url=url)
    llm_chain = get_openassistant_model()

    database_provider = database_utils.AWSS3Provider(
        bucket_name=COMMENTS_BUCKET
    )

    database_provider.create_bucket()

    for comment in islice(generator, max_items):
        comment_assessment = llm_chain.run(
            rules=rules,
            post=comment.body
        )
        comment_assessment = comment_assessment.strip()
        # Add extra logic for parsing model...
        reviewed_comment = models.ReviewedComment(
            id=comment.id,
            username=comment.username,
            body=comment.body,
            flag=comment_assessment[:4],
        )
        # Save to database
        object_data = reviewed_comment.dict()
        database_provider.save_object(object_data)

