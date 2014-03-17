from scrapy.spider import Spider

class WikipediaSpider(Spider):
    name = "Wikipedia"
    allowed_domains = ["wikipedia.org"]
    start_urls = (
        'http://www.wikipedia.org/',
        )

    def parse(self, response):
        pass 
