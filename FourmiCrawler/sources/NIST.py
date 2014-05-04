from source import Source
from scrapy import log
from scrapy.http import Request
from scrapy.selector import Selector
from FourmiCrawler.items import Result


class NIST(Source):
    website = "http://webbook.nist.gov/*"  

    search = 'cgi/cbook.cgi?Name=%s&Units=SI&cTG=on&cTC=on&cTP=on'

    def __init__(self):
        Source.__init__(self)

    def parse(self, reponse):
        pass

    def new_compound_request(self, compound):
        return Request(url=self.website[:-1] + self.search % compound,
                       callback=self.parse)
