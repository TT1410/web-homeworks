import json
from time import sleep

import scrapy
from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field


class AuthorItem(Item):
    fullname = Field()
    born_date = Field()
    born_location = Field()
    description = Field()


class QuoteItem(Item):
    author = Field()
    quote = Field()
    tags = Field()


class Pipeline:
    def open_spider(self, spider):
        self.items_to_export = {
            "quotes": [],
            "authors": []
        }

    def close_spider(self, spider):
        for filename, data in self.items_to_export.items():
            with open(f"{filename}.json", "w", encoding="utf-8") as fp:
                json.dump(data, fp, ensure_ascii=False)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if isinstance(item, AuthorItem):
            self.items_to_export['authors'].append(adapter.asdict())
        elif isinstance(item, QuoteItem):
            self.items_to_export['quotes'].append(adapter.asdict())

        return item


class QuotesSpider(scrapy.Spider):
    name = 'quotes_and_authors'
    custom_settings = {
        "ITEM_PIPELINES": {Pipeline: 300}
    }
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield QuoteItem(
                tags=quote.xpath("div[@class='tags']/a/text()").extract(),
                author=quote.xpath("span/small/text()").get().strip(),
                quote=quote.xpath("span[@class='text']/text()").get().strip()
            )

            yield scrapy.Request(
                self.start_urls[0] + quote.xpath("span/a/@href").get(),
                callback=self.get_author
            )

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def get_author(self, response):
        body = response.xpath('/html//div[@class="author-details"]')

        yield AuthorItem(
            fullname=body.xpath('h3[@class="author-title"]/text()').get().strip(),
            born_date=body.xpath('p/span[@class="author-born-date"]/text()').get().strip(),
            born_location=body.xpath('p/span[@class="author-born-location"]/text()').get().strip(),
            description=body.xpath('div[@class="author-description"]/text()').get().strip(),
        )


def main() -> None:
    # runner = CrawlerRunner()
    #
    # runner.crawl(QuotesSpider)


    process = CrawlerProcess()
    process.crawl(QuotesSpider)

    process.start()


if __name__ == '__main__':
    main()

