import json
from pathlib import Path
import configparser

from mongoengine import connect, Document, CASCADE
from mongoengine.fields import ListField, StringField, ReferenceField


config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('MONGO_DB', 'user')
mongodb_pass = config.get('MONGO_DB', 'password')
db_name = config.get('MONGO_DB', 'db_name')
domain = config.get('MONGO_DB', 'host')
port = config.get('MONGO_DB', 'port')


URI = (f"mongodb://{mongo_user}:{mongodb_pass}@{domain}:{port}/{db_name}?"
       "ssl=true&replicaSet=atlas-lhkelk-shard-0&authSource=admin&retryWrites=true&w=majority")

# connect to cluster on AtlasDB with connection string
connect(host=URI, ssl=True)


class Author(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField()
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField()

    meta = {'allow_inheritance': True}


class FormatQuotes:
    default_user: int = 1
    model_quote: str = 'quote.quote'
    model_tag: str = 'quote.tag'
    model_author: str = 'quote.author'

    def __init__(self, filename: str, django_project: str) -> None:
        self.file = Path(__file__).parent.parent / django_project / filename
        self.format_quotes = []
        self.format_tags = []
        self.format_authors = []

        self._tags = {}
        self._authors = {}

    def _get_author(self, author: Author) -> int:
        id_ = self._authors.get(author.fullname)

        if not id_:
            id_ = len(self.format_authors) + 1

            self._authors[author.fullname] = id_
            self.format_authors.append(
                {
                    "model": self.model_author,
                    "pk": id_,
                    "fields": {
                        "user_id": self.default_user,
                        "fullname": author.fullname,
                        "born_date": author.born_date,
                        "born_location": author.born_location,
                        "description": author.description
                    }
                }
            )
        return id_

    def _get_tags(self, tags: list[str]) -> list[int]:
        tag_ids = []

        for tag in tags:
            id_ = self._tags.get(tag)

            if not id_:
                id_ = len(self.format_tags) + 1

                self._tags[tag] = id_
                self.format_tags.append(
                    {
                        "model": self.model_tag,
                        "pk": id_,
                        "fields": {
                            "name": tag
                        }
                    }
                )
            tag_ids.append(id_)

        return tag_ids

    def _write_to_file(self) -> None:
        data = self.format_tags
        data.extend(self.format_authors)
        data.extend(self.format_quotes)

        with open(self.file, 'w', encoding='utf-8') as fp:
            json.dump(data, fp=fp, ensure_ascii=False, indent=4)

    def run(self) -> None:
        for num, item in enumerate(Quote.objects.all(), 1):
            self.format_quotes.append(
                {
                    "model": self.model_quote,
                    "pk": num,
                    "fields": {
                        "user_id": self.default_user,
                        "quote": item.quote.lstrip('“').rstrip('”'),
                        "author": self._get_author(item.author),
                        "tags": self._get_tags(item.tags)
                    }
                }
            )

        self._write_to_file()


if __name__ == '__main__':
    file_name = "data_migrate.json"
    django_project = 'quotes'

    format_data = FormatQuotes(file_name, django_project)
    format_data.run()

    print(f"\nJson file for migrating from mongodb to postgresql: {format_data.file}\n\n"
          "To migrate data run this commands in console.\n"
          f"Run command: cd {django_project}\n"
          f"Run command: python manage.py loaddata {file_name}\n"
          "\n(Be careful, existing quotes in the database will be overwritten with new ones!)")
