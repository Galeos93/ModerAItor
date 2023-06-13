"""Integration with Reddit website.

Notes
-----
To connect to Reddit's Moderaitor app, you need to set the `praw_client_id`
and the `praw_client_secret` credentials as secret files.

"""
import os
import typing

import praw
from praw.models import Comment, MoreComments

from moderaitor.models import BaseComment

SECRETS_PATH = os.getenv("SECRETS_PATH", "/run/secrets/")

def _get_client_id():
    with open(f"{SECRETS_PATH}praw_client_id", "r") as f_hdl:
        return f_hdl.read().strip()

def _get_client_secret():
    with open(f"{SECRETS_PATH}praw_client_secret", "r") as f_hdl:
        return f_hdl.read().strip()

def setup_client():
    reddit = praw.Reddit(
        user_agent="linux:moderaitor:v0.1",
        client_id=_get_client_id(),
        client_secret=_get_client_secret(),
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
        if isinstance(comment, MoreComments):
            continue
        yield parse_comment(comment)
