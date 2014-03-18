from scrapy.spider import Spider

class ChemspiderSpider(Spider):
    name = "Chemspider"
    allowed_domains = ["chemspider.com"]

    def __init__(self, compound=None, *args, **kwargs):
        super(ChemspiderSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["http://chemspiderapiurl/something/%s" % compound] #[TODO] - Give an logical start url.

    def parse(self, response):
        pass 
