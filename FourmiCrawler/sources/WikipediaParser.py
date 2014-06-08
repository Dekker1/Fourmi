import re

from scrapy.http import Request
from scrapy import log
from scrapy.selector import Selector

from source import Source
from FourmiCrawler.items import Result


class WikipediaParser(Source):
    """ Wikipedia scraper for chemical properties

    This parser parses Wikipedia info boxes (also bordered) to obtain properties and their values.
     It also returns requests with other external sources which contain information on parsed subject.
    """

    website = "http://en.wikipedia.org/wiki/*"
    __spider = None
    searched_compounds = []

    cfg = {}

    def __init__(self, config={}):
        Source.__init__(self, config)
        self.cfg = config

    def parse(self, response):
        """ Distributes the above described behaviour """
        log.msg('A response from %s just arrived!' % response.url, level=log.DEBUG)
        sel = Selector(response)
        compound = sel.xpath('//h1[@id="firstHeading"]//span/text()').extract()[0]  # makes sure to use main page
        if compound in self.searched_compounds:
            return None
        else:
            items = self.parse_infobox(sel)
            self.searched_compounds.append(compound)
            return items

    def parse_infobox(self, sel):
        """ scrape data from infobox on wikipedia. """
        items = []

        # be sure to get chembox (wikipedia template)
        tr_list = sel.xpath('.//table[@class="infobox bordered"]//td[not(@colspan)]'). \
            xpath('normalize-space(string())')
        prop_names = tr_list[::2]
        prop_values = tr_list[1::2]
        for i, prop_name in enumerate(prop_names):
            item = self.newresult(
                attribute=prop_name.extract().encode('utf-8'),
                value=prop_values[i].extract().encode('utf-8')
            )
            items.append(item)
            log.msg('Wiki prop: |%s| |%s| |%s|' % (item['attribute'], item['value'], item['source']), level=log.DEBUG)

        #scrape the  drugbox (wikipedia template)
        tr_list2 = sel.xpath('.//table[@class="infobox"]//tr')
        log.msg('dit: %s' % tr_list2, level=log.DEBUG)
        for tablerow in tr_list2:
            log.msg('item: %s' % tablerow.xpath('./th').xpath('normalize-space(string())'), level=log.DEBUG)
            if tablerow.xpath('./th').xpath('normalize-space(string())') and tablerow.xpath('./td').xpath(
                    'normalize-space(string())'):
                item = self.newresult(
                    attribute=tablerow.xpath('./th').xpath('normalize-space(string())').extract()[0].encode('utf-8'),
                    value=tablerow.xpath('./td').xpath('normalize-space(string())').extract()[0].encode('utf-8'),
                )
                items.append(item)
                log.msg(
                    'Wiki prop: |attribute: %s| |value: %s| |%s|' % (item['attribute'], item['value'], item['source']),
                    level=log.DEBUG)

        items = filter(lambda a: a['value'] != '', items)  # remove items with an empty value
        item_list = self.clean_items(items)

        identifiers = self.get_identifiers(sel)

        #add extra sources to scrape from as requests
        for i, identifier in enumerate(identifiers):
            request = None
            #discard internal wikipedia links
            if re.match('//en\.wikipedia', identifier):
                log.msg('Found link to Wikipedia, this is not something to scrape: %s' % identifier, level=log.WARNING)
            #fix links starting with '//www.'
            elif re.match('/{2}', identifier):
                identifier = re.sub("/{2}", "http://", identifier)
                request = Request(identifier)
            else:
                request = Request(identifier)
            log.msg('New identifier found, request: %s' % identifier, level=log.DEBUG)
            item_list.append(request)

        return item_list

    def new_compound_request(self, compound):
        return Request(url=self.website[:-1] + compound, callback=self.parse)

    @staticmethod
    def clean_items(items):
        """ clean up properties using regex, makes it possible to split the values from the units """
        for item in items:
            value = item['value']
            m = re.search('F;\s(\d+[\.,]?\d*)', value)  # clean up numerical Kelvin value (after F)
            if m:
                item['value'] = m.group(1) + " K"
            m = re.match('(\d+[\.,]?\d*)\sJ\sK.+mol', value)  # clean up J/K/mol values
            if m:
                item['value'] = m.group(1) + " J/K/mol"
        return items

    @staticmethod
    def get_identifiers(sel):
        """ find external links, named 'Identifiers' to different sources. """
        links = sel.xpath('//span[contains(concat(" ",normalize-space(@class)," "),"reflink")]/a'
                          '[contains(concat(" ",normalize-space(@class)," "),"external")]/@href').extract()
        return links

    def newresult(self, attribute, value):
        return Result({
            'attribute': attribute,
            'value': value,
            'source': 'Wikipedia',
            'reliability': self.cfg['reliability'],
            'conditions': ''
            })
