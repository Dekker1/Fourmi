from scrapy.http import Request
from parser import Parser
from scrapy.selector import Selector
from FourmiCrawler.items import Result

class WikipediaParser(Parser):

    website = "http://en.wikipedia.org/wiki/*"
    __spider = None

    #def __init__(self, csid):
    #    self.website = "http://en.wikipedia.org/wiki/{id}".format(id=csid)

    def parse(self, response):
        print response.url
        #self.log('A response from %s just arrived!' % response.url)
        sel = Selector(response)
        items = []
        item = Result()
        item['attribute']="Melting point"
        item['value']= sel.xpath('//tr/td/a[@title="Melting point"]/../../td[2]/text()').extract() # ('//tr[contains(@href, "/wiki/Melting_point")]/text()').extract()
        item['source']= "Wikipedia"
        items.append(item)
        print item['attribute']
        print item['value']
        print item['source']
        return items

    def getmeltingpoint(self, sel):
        item=Result()
        item['attribute']="Melting point"
        item['value']= sel.xpath('//tr/td/a[@title="Melting point"]/../../td[2]/text()').extract() # ('//tr[contains(@href, "/wiki/Melting_point")]/text()').extract()
        item['source']= "Wikipedia"
        return item

    def new_compound_request(self, compound):
        return Request(url=self.website[:-1] + compound, callback=self.parse)