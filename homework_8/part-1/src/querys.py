import re
from typing import Optional

from .models import (
    Author,
    Quote,
)
from .cache_redis import cache


@cache
def search_one_author_from_name(name: str) -> Optional[Author]:
    """
    Searches for the author by partial or complete match of the full name
    """
    return Author.objects(fullname__exact=name).first() or Author.objects(fullname__istartswith=name).first()


@cache
def get_quotes_from_author(name: str) -> str:
    author = search_one_author_from_name(name)

    if not author:
        return f"Author named \"{name}\" not found"

    quotes = Quote.objects(author=author)

    if not quotes:
        return f"The author \"{author.fullname}\" has no quotations"

    return (
        f"Quotes from the author {author.fullname}:\n"
        +
        '\n'.join(['\t' + quote.quote for quote in quotes])
    )


@cache
def get_quotes_from_tags(tags: list[str] | str) -> str:
    quotes = (
        Quote.objects(tags__in=tags)
            if isinstance(tags, list) else
        Quote.objects(tags=tags)
    )

    if not quotes and isinstance(tags, str):
        quotes = Quote.objects(
            tags=re.compile(fr'^{tags}', flags=re.IGNORECASE)
        )

    if not quotes:
        return f"No quotes found for tag/tags: \"{tags}\""

    return "Quotes:\n" + (
        '\n'.join(['\t' + quote.quote for quote in quotes])
    )
