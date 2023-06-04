"""Integration with Reddit website.

Notes
-----
To connect to Reddit's Moderaitor app, you need to set the `praw_client_id`
and the `praw_client_secret` environment variables.

"""
import typing

import praw
from praw.models import Comment

from moderaitor.models import BaseComment

def setup_client():
    reddit = praw.Reddit(
        user_agent="linux:moderaitor:v0.1",
    )
    return reddit

def parse_comment(comment: Comment) -> BaseComment:
    username = str(comment.author)
    return BaseComment(username=username, body=comment.body, id=comment.id)

def generate_comments(url: str) -> typing.Generator[BaseComment, None, None]:
    client = setup_client()
    submission = client.submission(url=url)
    all_comments = submission.comments.list()
    for comment in all_comments:
        yield parse_comment(comment)
