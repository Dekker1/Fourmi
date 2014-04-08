from parser import Parser
from scrapy import log
from scrapy.http import Request
from scrapy.selector import Selector
from FourmiCrawler.items import Result
from ChemSpider_token import TOKEN #TODO: move the token elsewhere

"""
This parser will manage searching for chemicals through the ChemsSpider API,
and parsing the resulting ChemSpider page. 
The token required for the API should be in a configuration file somewhere.
"""
class ChemSpider(Parser):
    
    website = "http://www.chemspider.com/*"
    __spider = 'ChemSpider'

    search = "Search.asmx/SimpleSearch?query=%s&token=%s"

    print "ChemSpider start"
    log.msg('chemspider start', level=log.DEBUG)

    def parse(self, response):
        sel = Selector(response)
        log.msg('chemspider parse', level=log.DEBUG)
        print "ChemSpider parse"
        pass
    
    def new_compound_request(self,compound):
        searchurl = self.website[:-1] + self.search % (compound, TOKEN)
        log.msg('chemspider compound', level=log.DEBUG)
        print "ChemSpider compound"
        return Request(url=searchurl, callback=self.parse)
