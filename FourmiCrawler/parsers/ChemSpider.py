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
    extendedinfo = "MassSpecAPI.asmx/GetExtendedCompoundInfo?csid=%s&token=052bfd06-5ce4-43d6-bf12-89eabefd2338"

    ignore_list = []

    def parse(self, response):
        sel = Selector(response)
        requests = []
        requests_synonyms = self.parse_synonyms(sel)
        requests.extend(requests_synonyms)
        requests_properties = self.parse_properties(sel)
        requests.extend(requests_properties)
        for wiki_url in sel.xpath('.//p[@class="syn"][strong]/a[@title="Wiki"]/@href').extract():
            requests.append( Request(url=wiki_url) )

        return requests

    def parse_properties(self, sel):
        requests = []
        properties = []

        td_list = sel.xpath('.//table[@id="acdlabs-table"]//td').xpath('normalize-space(string())')
        prop_names = td_list[::2]
        prop_values = td_list[1::2]
        for i, prop_name in enumerate(prop_names):
            new_prop = Result({
                'attribute': prop_name.extract().encode('utf-8'),
                'value': prop_values[i].extract().encode('utf-8'),
                'source': 'ChemSpider Predicted - ACD/Labs Tab',
                'reliability': '',
                'conditions': ''
                       })
            properties.append(new_prop)
            log.msg('CS prop: |%s| |%s| |%s|' \
            % (new_prop['attribute'],new_prop['value'], new_prop['source']),
            level=log.DEBUG)

        scraped_list = sel.xpath('.//li[span="Experimental Physico-chemical Properties"]//li/table/tr/td')
        if not scraped_list:
            return properties
        property_name = scraped_list.pop(0).xpath('span/text()').extract()[0].rstrip()
        for line in scraped_list:
            if line.xpath('span/text()'):
                property_name = line.xpath('span/text()').extract()[0].rstrip()
            else:
                new_prop = Result({
                    'attribute': property_name,
                    'value': line.xpath('text()').extract()[0].rstrip(),
                    'source': line.xpath('strong/text()').extract()[0].rstrip(),
                    'reliability': '',
                    'conditions': ''
                           })
                properties.append(new_prop)
                log.msg('CS prop: |%s| |%s| |%s|' \
                % (new_prop['attribute'],new_prop['value'], new_prop['source']),
                level=log.DEBUG)

        return properties

    def parse_synonyms(self, sel):
        requests = []
        synonyms = []
        for syn in sel.xpath('//p[@class="syn"][strong]'):
            name = syn.xpath('strong/text()').extract()[0]
            synonyms.append(self.new_synonym(syn, name, 'expert'))
        for syn in sel.xpath(
                        '//p[@class="syn"][span[@class="synonym_confirmed"]]'):
            name = syn.xpath(
                        'span[@class="synonym_confirmed"]/text()').extract()[0]
            synonyms.append(self.new_synonym(syn, name, 'user'))
        for syn in sel.xpath('//p[@class="syn"][span[@class=""]]'):
            name = syn.xpath('span[@class=""]/text()').extract()[0]
            synonyms.append(self.new_synonym(syn, name, 'nonvalidated'))

        for syn in synonyms:
            if (syn['category'] == 'expert' and syn['language'] == 'English'):
                log.msg('CS emit synonym: %s' % syn['name'], level=log.DEBUG)
                self._Parser__spider.get_synonym_requests(syn['name'])

        return requests

    def new_synonym(self, sel, name, category):
        self.ignore_list.append(name)
        language = sel.xpath('span[@class="synonym_language"]/text()').extract()
        if language:
            language = language[0][1:-1]
        else:
            language = 'English'
        synonym = {
                'name': name,
                'category': category,
                'language': language
                }
        log.msg('CS synonym: %s (%s) (%s)' % (name, category, language),
                level=log.DEBUG)
        return synonym

    def parse_extendedinfo(self, response):
        sel = Selector(response)
        properties = []
        names = sel.xpath('*').xpath('name()').extract()
        values = sel.xpath('*').xpath('text()').extract()
        for (name, value) in zip(names,values):
            result = Result({
                    'attribute': name,
                    'value': value,
                    'source': 'ChemSpider',
                    'reliability': '',
                    'conditions': ''
                    })
            properties.append(result)
        return properties

    def parse_searchrequest(self, response):
        sel = Selector(response)
        log.msg('chemspider parse_searchrequest', level=log.DEBUG)
        sel.register_namespace('cs', 'http://www.chemspider.com/')
        csid = sel.xpath('.//cs:int/text()').extract()[0]
        #TODO: handle multiple csids in case of vague search term
        structure_url = self.website[:-1] + self.structure % csid
        extendedinfo_url = self.website[:-1] + self.extendedinfo % csid
        log.msg('chemspider URL: %s' % structure_url, level=log.DEBUG)
        return [Request(url=structure_url, callback=self.parse),
                Request(url=extendedinfo_url, callback=self.parse_extendedinfo)]
    
    def new_compound_request(self,compound):
        if compound in self.ignore_list: #TODO: add regular expression
            return None
        searchurl = self.website[:-1] + self.search % compound
        log.msg('chemspider compound', level=log.DEBUG)
        return Request(url=searchurl, callback=self.parse_searchrequest)
