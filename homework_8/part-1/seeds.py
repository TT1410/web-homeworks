import json

from src.models import (
    Author,
    Quote,
)
from src.querys import search_one_author_from_name


def upload_authors(file: str) -> None:
    with open(file, "r", encoding="utf-8") as fp:
        authors = json.load(fp)

    [Author(**author).save() for author in authors]


def upload_qoutes(file: str) -> None:
    with open(file, "r", encoding="utf-8") as fp:
        qoutes = json.load(fp)

    for qoute in qoutes:
        Quote(
            author=search_one_author_from_name(
                qoute.pop("author")
            ),
            **qoute
        ).save()


if __name__ == '__main__':
    upload_authors("authors.json")
    upload_qoutes("qoutes.json")
