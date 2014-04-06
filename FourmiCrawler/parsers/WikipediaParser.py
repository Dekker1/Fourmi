import parser
from scrapy.selector import Selector
from FourmiCrawler.items import Result

class WikipediaParser:

    website = "http://en.wikipedia.org/wiki/Methane"
    __spider = "WikipediaParser"

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
