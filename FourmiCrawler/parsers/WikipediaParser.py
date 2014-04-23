from scrapy.http import Request
from scrapy import log
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
    searched_compounds = []

    def __init__(self):
        pass

    def parse(self, response):
        log.msg('A response from %s just arrived!' % response.url, level=log.DEBUG)
        sel = Selector(response)
        compound = sel.xpath('//h1[@id="firstHeading"]//span/text()').extract()[0]
        if compound in self.searched_compounds:
            return None
        else:
            items = self.parse_infobox(sel)
            self.searched_compounds.append(compound)
            return items

    def parse_infobox(self, sel):

        items = []

        tr_list = sel.xpath('.//table[@class="infobox bordered" or @class="infobox"]//td[not(@colspan)]').xpath('normalize-space(string())')
        prop_names = tr_list[::2]
        prop_values = tr_list[1::2]
        for i, prop_name in enumerate(prop_names):
            item = Result({
                'attribute': prop_name.extract().encode('utf-8'),
                'value': prop_values[i].extract().encode('utf-8'),
                'source': "Wikipedia",
                'reliability': "",
                'conditions': ""
            })
            items.append(item)
            log.msg('Wiki prop: |%s| |%s| |%s|' % (item['attribute'], item['value'], item['source']), level=log.DEBUG)
        items = filter(lambda a: a['value'] != '', items)  # remove items with an empty value
        itemlist = self.cleanitems(items)

        identifiers = self.get_identifiers(sel)

        for i, identifier in enumerate(identifiers):
            if re.match('//en\.wikipedia',identifier):
                log.msg('Found link to wikipedia, this is not something to scrape: %s' % identifier, level=log.WARNING)
            elif re.match('/{2}',identifier):
                identifier = re.sub("/{2}", "http://", identifier)
                request = Request(identifier)
            else:
                request = Request(identifier)
            log.msg('New identifier found, request: %s' % identifier, level=log.DEBUG)
            itemlist.append(request)

        return itemlist

    def new_compound_request(self, compound):
        return Request(url=self.website[:-1] + compound, callback=self.parse)

    def cleanitems(self, items):
        for item in items:
            value = item['value']
            m = re.search('F;\s(\d+[\.,]?\d*)', value)
            if m:
                item['value'] = m.group(1) + " K"
            m = re.match('(\d+[\.,]?\d*)\sJ\sK.+mol', value)
            if m:
                item['value'] = m.group(1) + " J/K/mol"
        return items

    def get_identifiers(self, sel):
        links = sel.xpath('//span[contains(concat(" ",normalize-space(@class)," "),"reflink")]/a'
                          '[contains(concat(" ",normalize-space(@class)," "),"external")]/@href').extract()
        return links