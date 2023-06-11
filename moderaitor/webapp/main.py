from itertools import islice

from fastapi import FastAPI
from pydantic import BaseModel

from moderaitor import database_utils
from moderaitor import scrapper
from moderaitor import models
from moderaitor.llm.openassistant import get_model as get_openassistant_model
from moderaitor.cli import __app_name__, __version__

# Import any necessary libraries for web scraping and comment moderation

app = FastAPI()

class CommentModerationRequest(BaseModel):
    url: str
    explain: bool
    rules: str
    max_comments: int


@app.post("/moderate_post/")
def moderate_comments(request: CommentModerationRequest):
    # Extract the URL, explain, and rules from the request
    url = request.url
    explain = request.explain
    rules = request.rules
    max_items = request.max_comments

    generator = scrapper.generator_factory(url=url)
    llm_chain = get_openassistant_model()

    database_provider = database_utils.AWSS3Provider(
        bucket_name="quarantined-comments"
    )
    # database_provider.create_bucket()

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

    return {"message": "Comments moderated successfully"}
