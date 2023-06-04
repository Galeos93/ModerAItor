import typing
from urllib.parse import urlparse

from moderaitor.scrapper import integrations
from moderaitor.models import BaseComment


def generator_factory(url: str) -> typing.Generator[BaseComment, None, None]:
    uri = urlparse(url) 
    netloc = uri.netloc

    if netloc == 'www.reddit.com':
        generator = integrations.reddit.generate_comments(url)
    else:
        raise ValueError(f"Integration for {netloc} is not available.")

    return generator