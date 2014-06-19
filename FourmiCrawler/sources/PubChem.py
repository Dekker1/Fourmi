import re

from scrapy.http import Request
from scrapy import log
from scrapy.selector import Selector

from source import Source
from FourmiCrawler.items import Result


class PubChem(Source):
    """ PubChem scraper for chemical properties

        This parser parses the part on PubChem pages that gives Chemical and Physical properties of a substance,
        including sources of the values of properties.
    """

    #PubChem has its data on compound name, properties and their values on different html pages, so different URLs used
    website = 'http://.*\\.ncbi\\.nlm\\.nih\\.gov/.*'
    website_www = 'http://www.ncbi.nlm.nih.gov/*'
    website_pubchem = 'http://pubchem.ncbi.nlm.nih.gov/.*'
    search = 'pccompound?term=%s'
    data_url = 'toc/summary_toc.cgi?tocid=27&cid=%s'

    __spider = None
    searched_compounds = set()

    def __init__(self, config):
        Source.__init__(self, config)
        self.cfg = config

    def parse(self, response):
        """
        Distributes the above described behaviour
        :param response: The incoming search request
        :return Returns the found properties if response is unique or returns none if it's already known
        """
        requests = []
        log.msg('A response from %s just arrived!' % response.url, level=log.DEBUG)

        sel = Selector(response)
        compound = sel.xpath('//h1/text()').extract()[0]
        if compound in self.searched_compounds:
            return None

        self.searched_compounds.update(compound)
        raw_synonyms = sel.xpath('//div[@class="smalltext"]/text()').extract()[0]
        for synonym in raw_synonyms.strip().split(', '):
            log.msg('PubChem synonym found: %s' % synonym, level=log.DEBUG)
            self.searched_compounds.update(synonym)
            self._spider.get_synonym_requests(synonym)
        log.msg('Raw synonyms found: %s' % raw_synonyms, level=log.DEBUG)

        n = re.search(r'cid=(\d+)', response.url)
        if n:
            cid = n.group(1)
        log.msg('cid: %s' % cid, level=log.DEBUG)   #getting the right id of the compound with which it can reach
                                                # the seperate html page which contains the properties and their values

        #using this cid to get the right url and scrape it
        requests.append(Request(url=self.website_pubchem[:-1] + self.data_url % cid, callback=self.parse_data))
        return requests

    def parse_data(self, response):
        """
        Parse data found in 'Chemical and Physical properties' part of a substance page.
        :param response: The response with the page to parse
        :return: requests: Returns a list of properties with their values, source, etc.
        """
        log.msg('parsing data', level=log.DEBUG)
        requests = []

        sel = Selector(response)
        props = sel.xpath('//div')

        for prop in props:
            prop_name = ''.join(prop.xpath('b/text()').extract()) # name of property that it is parsing
            if prop.xpath('a'):     # parsing for single value in property
                prop_source = ''.join(prop.xpath('a/@title').extract())
                prop_value = ''.join(prop.xpath('a/text()').extract())
                new_prop = Result({
                    'attribute': prop_name,
                    'value': prop_value,
                    'source': prop_source,
                    'reliability': 'Unknown',
                    'conditions': ''
                })
                log.msg('PubChem prop: |%s| |%s| |%s|' %
                        (new_prop['attribute'], new_prop['value'],
                         new_prop['source']), level=log.DEBUG)
                requests.append(new_prop)
            elif prop.xpath('ul'):    # parsing for multiple values (list) in property
                prop_values = prop.xpath('ul//li')
                for prop_li in prop_values:
                    prop_value = ''.join(prop_li.xpath('a/text()').extract())
                    prop_source = ''.join(prop_li.xpath('a/@title').extract())
                    new_prop = Result({
                        'attribute': prop_name,
                        'value': prop_value,
                        'source': prop_source,
                        'reliability': 'Unknown',
                        'conditions': ''
                    })
                    log.msg('PubChem prop: |%s| |%s| |%s|' %
                        (new_prop['attribute'], new_prop['value'],
                         new_prop['source']), level=log.DEBUG)
                    requests.append(new_prop)

        return requests

    def parse_searchrequest(self, response):
        """
        This function parses the response to the new_compound_request Request
        :param response: the Response object to be parsed
        :return: A Request for the compound page or what self.parse returns in
                 case the search request forwarded to the compound page
        """

        #check if pubchem forwarded straight to compound page
        m = re.match(self.website_pubchem, response.url)
        if m:
            log.msg('PubChem search forwarded to compound page',
                    level=log.DEBUG)
            return self.parse(response)

        sel = Selector(response)

        results = sel.xpath('//div[@class="rsltcont"]')
        if results:
            url = results[0].xpath('div/p/a[1]/@href')
        else:
            log.msg('PubChem search found nothing or xpath failed',
                    level=log.DEBUG)
            return None

        if url:
            url = 'http:' + ''.join(url[0].extract())
            log.msg('PubChem compound page: %s' % url, level=log.DEBUG)
        else:
            log.msg('PubChem search found results, but no url in first result',
                    level=log.DEBUG)
            return None

        return Request(url=url, callback=self.parse)

    def new_compound_request(self, compound):
        return Request(url=self.website_www[:-1] + self.search % compound,
                       callback=self.parse_searchrequest)
