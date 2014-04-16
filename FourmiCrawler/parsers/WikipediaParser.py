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
        items = self.parse_infobox(sel)
        return items

    def parse_infobox(self, sel):
        items=[]
        tr_list = sel.xpath('.//table[@class="infobox bordered"]//td[not(@colspan)]').xpath('normalize-space(string())')
        prop_names = tr_list[::2]
        prop_values = tr_list[1::2]
        for i, prop_name in enumerate(prop_names):
            item = Result()
            item['attribute'] = prop_name.extract().encode('utf-8')
            item['value'] = prop_values[i].extract().encode('utf-8')
            item['source'] = "Wikipedia"
            items.append(item)
            print "new: " + item['attribute']
            print item['value']
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

    def getdensity(self, sel):
        item=Result()
        item['attribute']="Density"
        item['value']= sel.xpath('//tr/td/a[@title="Density"]/../../td[2]/text()').extract() # ('//tr[contains(@href, "/wiki/Melting_point")]/text()').extract()
        item['source']= "Wikipedia"
        print item['value']
        return item

    def getheatcapacity(self, sel):
        item=Result()
        item['attribute']="Specific heat capacity"
        item['value']= sel.xpath('//tr/td/a[@title="Specific heat capacity"]/../../td[2]/text()').extract() # ('//tr[contains(@href, "/wiki/Melting_point")]/text()').extract()
        item['source']= "Wikipedia"
        print item['value']
        return item

    def getmolarentropy(self, sel):
        item=Result()
        item['attribute']="Standard molar entropy"
        item['value']= sel.xpath('//tr/td/a[@title="Standard molar entropy"]/../../td[2]/text()').extract() # ('//tr[contains(@href, "/wiki/Melting_point")]/text()').extract()
        item['source']= "Wikipedia"
        print item['value']
        return item

    def getchemspider(self, sel):
        link=sel.xpath('//tr/td/a[@title="ChemSpider"]/../../td[2]/span/a/@href').extract()[0] # ('//tr[contains(@href, "/wiki/Melting_point")]/text()').extract()
        print link
        return link