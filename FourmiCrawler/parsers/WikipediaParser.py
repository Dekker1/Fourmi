from scrapy.http import Request
from parser import Parser
from scrapy.selector import Selector
from FourmiCrawler.items import Result

class WikipediaParser(Parser):

    website = "http://en.wikipedia.org/wiki/*"
    __spider = None

    print "test1"
    #def __init__(self, csid):
    #    self.website = "http://en.wikipedia.org/wiki/{id}".format(id=csid)

    def parse(self, response):
        print "test1"
        #self.log('A response from %s just arrived!' % response.url)
    #def parse():
        sel = Selector("http://en.wikipedia.org/wiki/Methane")
        items = []
        item = Result()
        item['attribute']="Melting point"
        item['value']=site.xpath('//tr[contains(@href, "/wiki/Melting_point")]/text()').extract()
        item['source']= self.website
        items.append(item)
        print item['attribute']
        print item['value']
        print item['source']
        print "test"
        return items

    def new_compound_request(self, compound):
        return Request(url=self.website[:-1] + compound, callback=self.parse)