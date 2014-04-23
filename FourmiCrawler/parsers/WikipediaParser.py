from scrapy.http import Request
from parser import Parser
from scrapy.selector import Selector
from FourmiCrawler.items import Result
import re

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
            item['reliability'] = ""
            item['conditions'] = ""
            items.append(item)
            #print "new: " + item['attribute']
            #print item['value']
        items=filter(lambda a: a['value']!='', items) #remove items with an empty value
        #print items
        self.cleanitems(items)
        return items

    def new_compound_request(self, compound):
        return Request(url=self.website[:-1] + compound, callback=self.parse)

    def cleanitems(self, items):
        for item in items:
            value=item['value']
            if re.search('F;\s(\d+[\.,]?\d*)', value):
                #print re.search('F;\s(\d+[\.,]?\d*)', value).group(1)
                item['value']=re.search('F;\s(\d+[\.,]?\d*)', value).group(1) + " K"
            if re.match('(\d+[\.,]?\d*)\sJ\sK.+mol', value):
                print item['value']
                item['value']=re.search('(\d+[\.,]?\d*)\sJ\sK.+mol', value).group(1) + " J/K/mol"
            print item['value']
        return items

    def getchemspider(self, sel):
        link=sel.xpath('//tr/td/a[@title="ChemSpider"]/../../td[2]/span/a/@href').extract()[0] # ('//tr[contains(@href, "/wiki/Melting_point")]/text()').extract()
        print link
        return link