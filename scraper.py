"""Scrapy-compatible scraping foundation; keep site-specific rules in spiders."""
import scrapy
from scrapy.crawler import CrawlerProcess

class GenericSpider(scrapy.Spider):
    name = "generic"
    allowed_domains = []
    start_urls = []

    def parse(self, response):
        yield {
            "url": response.url,
            "title": response.css("title::text").get(default="").strip(),
            "links": response.css("a::attr(href)").getall(),
        }

if __name__ == "__main__":
    CrawlerProcess().crawl(GenericSpider)
    CrawlerProcess().start()
