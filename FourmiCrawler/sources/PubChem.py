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

    # TO DO: make url variable with help of PubChem identifier ID / cid

    #website = "https://pubchem.ncbi.nlm.nih.gov/summary/summary.cgi?cid=297"            #contains name of compound but not all parsable data
    # website = "https://pubchem.ncbi.nlm.nih.gov/toc/summary_toc.cgi?tocid=27&cid=297"  #contains properties to parse


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




        return requests


    def parse_properties(self, sel):
        """ scrape data from 'Chemical and Physical Properties' box on PubChem. """
        items = []


        prop_names = sel.xpath('.//div[@id="d27"//div/b').\
            xpath('normalize-space(string())')
        prop_values = sel.xpath('.//div[@id="d27"//div/a').\
            xpath('normalize-space(string())')
        prop_sources = sel.xpath('.//div[@id="d27"//div/a[@title]').\
            xpath('normalize-space(string())')

        for i, prop_name in enumerate(prop_names):
            item = Result({
                'attribute': prop_name.extract().encode('utf-8'),
                'value': prop_values[i].extract().encode('utf-8'),
                'source': "PubChem: " + prop_sources[i].extract().encode('utf-8'),
                'reliability': "",
                'conditions': ""
            })
            items.append(item)

            print item

            log.msg('PubChem prop: |%s| |%s| |%s|' % (item['attribute'], item['value'], item['source']), level=log.DEBUG)

        items = filter(lambda a: a['value'] != '', items)  # remove items with an empty value
        # item_list = self.clean_items(items)


        return items

    def new_compound_request(self, compound):
        return Request(url=self.website_www[:-1] + self.search % compound, callback=self.parse)

    # @staticmethod
    # def clean_items(items):
    #     """ clean up properties using regex, makes it possible to split the values from the units """
    #     for item in items:
    #         value = item['value']
    #         m = re.search('F;\s(\d+[\.,]?\d*)', value)  # clean up numerical Kelvin value (after F)
    #         if m:
    #             item['value'] = m.group(1) + " K"
    #         m = re.match('(\d+[\.,]?\d*)\sJ\sK.+mol', value)  # clean up J/K/mol values
    #         if m:
    #             item['value'] = m.group(1) + " J/K/mol"
    #     return items
