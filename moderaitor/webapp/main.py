from itertools import islice
import logging
import os

from fastapi import FastAPI
from pydantic import BaseModel

from moderaitor import database_utils
from moderaitor import scrapper
from moderaitor import models
from moderaitor.llm.openassistant import get_model as get_openassistant_model
from moderaitor.cli import __app_name__, __version__

COMMENTS_BUCKET = os.getenv("COMMENTS_BUCKET", "quarantined-comments")

logging.basicConfig(level=logging.INFO)

app = FastAPI()

class CommentModerationRequest(BaseModel):
    url: str
    explain: bool = False
    rules: str
    max_comments: int = None


@app.post("/moderate_post/")
def moderate_comments(request: CommentModerationRequest):
    logger = logging.getLogger(__name__)

    url = request.url
    _ = request.explain
    rules = request.rules
    max_items = request.max_comments

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
        logger.info(reviewed_comment)
        # Save to database
        object_data = reviewed_comment.dict()
        database_provider.save_object(object_data)

    return {"message": "Comments moderated successfully"}
