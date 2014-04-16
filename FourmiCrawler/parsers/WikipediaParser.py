from scrapy.http import Request
from parser import Parser
from scrapy.selector import Selector
from FourmiCrawler.items import Result

class WikipediaParser(Parser):

# General notes:
# Redirects seem to not matter as Wikipedia returns the page the redirect forwards to
# although this might lead to scraping both the original and the redirect with the same data.

    website = "http://en.wikipedia.org/wiki/*"
    __spider = None

    #def __init__(self, csid):
    #    self.website = "http://en.wikipedia.org/wiki/{id}".format(id=csid)

    def parse(self, response):
        print response.url
        #self.log('A response from %s just arrived!' % response.url)
        sel = Selector(response)
        items = []
        meltingpoint = self.getmeltingpoint(sel)
        items.append(meltingpoint)
        boilingpoint = self.getboilingpoint(sel)
        chemlink = self.getchemspider(sel)
        items.append(boilingpoint)
        return items

    def new_compound_request(self, compound):
        return Request(url=self.website[:-1] + compound, callback=self.parse)

    def getmeltingpoint(self, sel):
        item=Result()
        item['attribute']="Melting point"
        item['value']= sel.xpath('//tr/td/a[@title="Melting point"]/../../td[2]/text()').extract() # ('//tr[contains(@href, "/wiki/Melting_point")]/text()').extract()
        item['source']= "Wikipedia"
        return item

    def getboilingpoint(self, sel):
        item=Result()
        item['attribute']="Boiling point"
        item['value']= sel.xpath('//tr/td/a[@title="Boiling point"]/../../td[2]/text()').extract() # ('//tr[contains(@href, "/wiki/Melting_point")]/text()').extract()
        item['source']= "Wikipedia"
        return item

    def getchemspider(self, sel):
        item=sel.xpath('//tr/td/a[@title="ChemSpider"]/../../td[2]/span/a/@href').extract() # ('//tr[contains(@href, "/wiki/Melting_point")]/text()').extract()
        print item
        return item