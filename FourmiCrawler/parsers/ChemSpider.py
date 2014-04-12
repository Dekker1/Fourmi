from parser import Parser
from scrapy import log
from scrapy.http import Request
from scrapy.selector import Selector
from FourmiCrawler.items import Result

"""
This parser will manage searching for chemicals through the ChemsSpider API,
and parsing the resulting ChemSpider page. 
The token required for the API should be in a configuration file somewhere.
"""
class ChemSpider(Parser):
    
    website = "http://www.chemspider.com/*"
    __spider = 'ChemSpider'

    search = "Search.asmx/SimpleSearch?query=%s&token=052bfd06-5ce4-43d6-bf12-89eabefd2338"
    structure = "Chemical-Structure.%s.html"

    def parse(self, response):
        sel = Selector(response)
        log.msg('chemspider parse', level=log.WARNING)

    def parse_searchrequest(self, response):
        sel = Selector(response)
        log.msg('chemspider parse_searchrequest', level=log.WARNING)
        sel.register_namespace('cs', 'http://www.chemspider.com/')
        csid = sel.xpath('.//cs:int/text()').extract()[0]
        #TODO: handle multiple csids in case of vague search term
        structure_url = self.website[:-1] + self.structure % csid
        log.msg('chemspider URL: %s' % structure_url, level=log.WARNING)
        return Request(structure_url, callback=self.parse)
    
    def new_compound_request(self,compound):
        searchurl = self.website[:-1] + self.search % compound
        log.msg('chemspider compound', level=log.WARNING)
        return Request(url=searchurl, callback=self.parse_searchrequest)
