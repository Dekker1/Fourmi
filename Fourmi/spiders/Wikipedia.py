from scrapy.spider import Spider

class WikipediaSpider(Spider):
    name = "Wikipedia"
    allowed_domains = ["wikipedia.org"]

    def __init__(self, compound=None, *args, **kwargs):
        super(WikipediaSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["http://wikipediaurl/something/%s" % compound] #[TODO] - Give an logical start url.

    def parse(self, response):
        pass 
