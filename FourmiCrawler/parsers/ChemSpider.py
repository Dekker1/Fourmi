from parser import Parser
from scrapy import log
from scrapy.http import Request
from scrapy.selector import Selector
from FourmiCrawler.items import Result

"""
This parser will manage searching for chemicals through the ChemsSpider API,
and parsing the resulting ChemSpider page. 
The token required for the API should be in a configuration file somewhere.
"""
class ChemSpider(Parser):
    
    website = "http://www.chemspider.com/*"

    search = "Search.asmx/SimpleSearch?query=%s&token=052bfd06-5ce4-43d6-bf12-89eabefd2338"
    structure = "Chemical-Structure.%s.html"

    ignore_list = []

    def parse(self, response):
        sel = Selector(response)
        requests = []
        requests_synonyms = self.parse_synonyms(sel)
        requests.extend(requests_synonyms)
        requests_properties = self.parse_properties(sel)
        requests.extend(requests_properties)
        for wiki_url in sel.xpath('.//a[@title="Wiki"]/@href').extract():
            requests.append( Request(url=wiki_url) )

        return requests

    def parse_properties(self, sel):
        requests = []
        properties = []

        td_list = sel.xpath('.//table[@id="acdlabs-table"]//td').xpath('normalize-space(string())')
        prop_names = td_list[::2]
        prop_values = td_list[1::2]
        for i, prop_name in enumerate(prop_names):
            new_prop = Result()
            new_prop['attribute'] = prop_name.extract().encode('utf-8')
            new_prop['value'] = prop_values[i].extract().encode('utf-8')
            new_prop['source'] = 'ChemSpider Predicted - ACD/Labs Tab'
            new_prop['reliability'] = None
            new_prop['conditions'] = None
            properties.append(new_prop)
            log.msg('CS prop: |%s| |%s| |%s|' \
            % (new_prop['attribute'],new_prop['value'], new_prop['source']),
            level=log.WARNING)

        scraped_list = sel.xpath('.//li[span="Experimental Physico-chemical Properties"]//li/table/tr/td')
        if not scraped_list:
            return None
        property_name = scraped_list.pop(0).xpath('span/text()').extract()[0].rstrip()
        for line in scraped_list:
            if line.xpath('span/text()'):
                property_name = line.xpath('span/text()').extract()[0].rstrip()
            else:
                new_prop = Result()
                new_prop['attribute'] = property_name
                new_prop['value'] = line.xpath('text()').extract()[0].rstrip()
                new_prop['source'] = line.xpath('strong/text()').extract()[0].rstrip()
                new_prop['reliability'] = None
                new_prop['conditions'] = None
                properties.append(new_prop)
                log.msg('CS prop: |%s| |%s| |%s|' \
                % (new_prop['attribute'],new_prop['value'], new_prop['source']),
                level=log.WARNING)

        return properties

    def parse_synonyms(self, sel):
        requests = []
        synonyms = []
        for syn in sel.xpath('//p[@class="syn"]/strong/text()').extract():
            synonyms.append( self.new_synonym( syn, 'high' ) )
        for syn in sel.xpath('//p[@class="syn"]/span[@class="synonym_confirmed"]/text()').extract():
            synonyms.append( self.new_synonym( syn, 'medium' ) )
        for syn in sel.xpath('//p[@class="syn"]/span[@class=""]/text()').extract():
            synonyms.append( self.new_synonym( syn, 'low' ) )

        for synonym in synonyms:
            if synonym['reliability'] == 'high':
                self._Parser__spider.get_synonym_requests(synonym['value'])

        return requests

    def new_synonym(self, name, reliability):
        log.msg('CS synonym: %s (%s)' % (name, reliability), level=log.WARNING)
        self.ignore_list.append(name)
        synonym = Result()
        synonym['attribute'] = 'synonym'
        synonym['value'] = name
        synonym['source'] = 'ChemSpider'
        synonym['reliability'] = reliability
        synonym['conditions'] = None
        return synonym


    def parse_searchrequest(self, response):
        sel = Selector(response)
        log.msg('chemspider parse_searchrequest', level=log.WARNING)
        sel.register_namespace('cs', 'http://www.chemspider.com/')
        csid = sel.xpath('.//cs:int/text()').extract()[0]
        #TODO: handle multiple csids in case of vague search term
        structure_url = self.website[:-1] + self.structure % csid
        log.msg('chemspider URL: %s' % structure_url, level=log.WARNING)
        return Request(structure_url, callback=self.parse)
    
    def new_compound_request(self,compound):
        if compound in self.ignore_list: #TODO: add regular expression
            return None
        searchurl = self.website[:-1] + self.search % compound
        log.msg('chemspider compound', level=log.WARNING)
        return Request(url=searchurl, callback=self.parse_searchrequest)
