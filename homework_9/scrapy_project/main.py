from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scrapy_project.spiders import QuotesSpider, AuthorsSpider


def main() -> None:
    process = CrawlerProcess(get_project_settings())

    process.crawl(QuotesSpider)
    process.crawl(AuthorsSpider)

    process.start()


if __name__ == '__main__':
    main()
