from scrapy.spider import Spider

class ChemspiderSpider(Spider):
    name = "Chemspider"
    allowed_domains = ["chemspider.com"]
    start_urls = (
        'http://www.chemspider.com/',
        )

    def parse(self, response):
        pass 
