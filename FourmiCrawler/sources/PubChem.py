from scrapy.http import Request
from scrapy import log
from source import Source
from scrapy.selector import Selector
from FourmiCrawler.items import Result
import re


class PubChem(Source):
    """ PubChem scraper for chemical properties

        This parser parses the part on PubChem pages that gives Chemical and Physical properties of a substance.
    """

    website = 'https://*.ncbi.nlm.nih.gov/*'
    website_www = 'https://www.ncbi.nlm.nih.gov/*'
    website_pubchem = 'https://pubchem.ncbi.nlm.nih.gov/*'
    search = 'pccompound?term=%s'
    data_url = 'toc/summary_toc.cgi?tocid=27&cid=%s'

    __spider = None
    searched_compounds = set()

    def __init__(self):
        Source.__init__(self)

    def parse(self, response):
        """ Distributes the above described behaviour """
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

        n = re.search(r'cid=(\d+)',response.url)
        if n:
            cid = n.group(1)
        log.msg('cid: %s' % cid, level=log.DEBUG)
        requests.append(Request(url=self.website_pubchem[:-1] + self.data_url % cid, callback=self.parse_data))

        return requests

    def parse_data(self, response):
        log.msg('parsing data', level=log.DEBUG)
        requests = []

        sel = Selector(response)
        props = sel.xpath('//div')

        for prop in props:
            prop_name = ''.join(prop.xpath('b/text()').extract())
            if prop.xpath('a'):
                prop_source = ''.join(prop.xpath('a/@title').extract())
                prop_value = ''.join(prop.xpath('a/text()').extract())
                new_prop = Result({
                    'attribute': prop_name,
                    'value': prop_value,
                    'source': prop_source,
                    'reliability': 'Unknown',
                    'conditions': ''
                })
                requests.append(new_prop)
            elif prop.xpath('ul'):
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
                    requests.append(new_prop)

        return requests


    def new_compound_request(self, compound):
        return Request(url=self.website_www[:-1] + self.search % compound, callback=self.parse)