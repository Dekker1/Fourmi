from parser import Parser
from scrapy import log
from scrapy.http import Request
from scrapy.selector import Selector
from FourmiCrawler.items import Result
import re

# [TODO] - Maybe clean up usage of '.extract()[0]', because it will raise an IndexError exception if the xpath matches nothing.

class ChemSpider(Parser):
"""ChemSpider scraper for synonyms and properties

This parser will manage searching for chemicals through the
ChemsSpider API, and parsing the resulting ChemSpider page.
The token required for the API should be in a configuration file
somewhere.
"""
    website = 'http://www.chemspider.com/*'

    # [TODO] - Save and access token of specific user.
    search = ('Search.asmx/SimpleSearch?query=%s&token='
        '052bfd06-5ce4-43d6-bf12-89eabefd2338')
    structure = 'Chemical-Structure.%s.html'
    extendedinfo = ('MassSpecAPI.asmx/GetExtendedCompoundInfo?csid=%s&token='
        '052bfd06-5ce4-43d6-bf12-89eabefd2338')

    ignore_list = []

    def parse(self, response):
        sel = Selector(response)
        requests = []
        requests_synonyms = self.parse_synonyms(sel)
        requests.extend(requests_synonyms)
        requests_properties = self.parse_properties(sel)
        requests.extend(requests_properties)

        return requests

    def parse_properties(self, sel):
        """scrape Experimental Data and Predicted ACD/Labs tabs"""
        requests = []
        properties = []

        # Predicted - ACD/Labs tab
        # [TODO] - test if tab contains data, some chemicals do not have data here
        td_list = sel.xpath('.//table[@id="acdlabs-table"]//td').xpath(
                                                'normalize-space(string())')
        prop_names = td_list[::2]
        prop_values = td_list[1::2]
        for (prop_name, prop_value) in zip(prop_names, prop_values):
            # [:-1] is to remove the colon at the end, [TODO] - test for colon
            prop_name = prop_name.extract().encode('utf-8')[:-1]
            prop_value = prop_value.extract().encode('utf-8')
            prop_conditions = ''

            # Match for condition in parentheses
            m = re.match(r'(.*) \((.*)\)', prop_name)
            if m:
                prop_name = m.group(1)
                prop_conditions = m.group(2)

            # Match for condition in value seperated by an 'at'
            m = re.match(r'(.*) at (.*)', prop_value)
            if m:
                prop_value = m.group(1)
                prop_conditions = m.group(2)

            new_prop = Result({
                'attribute': prop_name,
                'value': prop_value,
                'source': 'ChemSpider Predicted - ACD/Labs Tab',
                'reliability': 'Unknown',
                'conditions': prop_conditions
                })
            properties.append(new_prop)
            log.msg('CS prop: |%s| |%s| |%s|' %
                (new_prop['attribute'], new_prop['value'], new_prop['source']),
                level=log.DEBUG)

        # Experimental Data Tab, Physico-chemical properties in particular
        scraped_list = sel.xpath('.//li[span="Experimental Physico-chemical '
                                                'Properties"]//li/table/tr/td')
        if not scraped_list:
            return properties
        # Format is: property name followed by a list of values
        property_name = scraped_list.pop(0).xpath(
                                        'span/text()').extract()[0].rstrip()
        for line in scraped_list:
            if line.xpath('span/text()'):
                property_name = line.xpath('span/text()').extract()[0].rstrip()
            else:
                new_prop = Result({
                    'attribute': property_name[:-1],
                    'value': line.xpath('text()').extract()[0].rstrip(),
                    'source': line.xpath(
                                        'strong/text()').extract()[0].rstrip(),
                    'reliability': 'Unknown',
                    'conditions': ''
                           })
                properties.append(new_prop)
                log.msg('CS prop: |%s| |%s| |%s|' %
                    (new_prop['attribute'], new_prop['value'],
                    new_prop['source']), level=log.DEBUG)

        return properties

    def parse_synonyms(self, sel):
        """Scrape list of Names and Identifiers"""
        requests = []
        synonyms = []

        # Exact type for this is unknown, but equivalent to Validated by Expert
        for syn in sel.xpath('//p[@class="syn"][span[@class="synonym_cn"]]'):
            name = syn.xpath('span[@class="synonym_cn"]/text()').extract()[0]
            synonyms.append(self.new_synonym(syn, name, 'expert'))
        # These synonyms are labeled by ChemSpider as "Validated by Experts"
        for syn in sel.xpath('//p[@class="syn"][strong]'):
            name = syn.xpath('strong/text()').extract()[0]
            synonyms.append(self.new_synonym(syn, name, 'expert'))
        # These synonyms are labeled by ChemSpider as "Validated by Users"
        for syn in sel.xpath(
                        '//p[@class="syn"][span[@class="synonym_confirmed"]]'):
            name = syn.xpath(
                        'span[@class="synonym_confirmed"]/text()').extract()[0]
            synonyms.append(self.new_synonym(syn, name, 'user'))
        # These syonyms are labeled as "Non-validated" and assumed unreliable
        for syn in sel.xpath('//p[@class="syn"][span[@class=""]]'):
            name = syn.xpath('span[@class=""]/text()').extract()[0]
            synonyms.append(self.new_synonym(syn, name, 'nonvalidated'))

        # [TODO] - confirm if English User-Validated synonyms are OK too
        for syn in synonyms:
            if (syn['category'] == 'expert' and syn['language'] == 'English'):
                log.msg('CS emit synonym: %s' % syn['name'], level=log.DEBUG)
                self._Parser__spider.get_synonym_requests(syn['name'])

        return requests

    def new_synonym(self, sel, name, category):
        """Scrape for a single synonym at a given HTML tag"""
        self.ignore_list.append(name)
        language = sel.xpath('span[@class="synonym_language"]/text()')
        if language:
            # The [1:-1] is to remove brackets around the language name
            language = language.extract()[0][1:-1]
        else:
            # If language is not given, English is assumed, [TODO] - confirm
            language = 'English'
        log.msg('CS synonym: %s (%s) (%s)' % (name, category, language),
                level=log.DEBUG)
        references = []
        # A synonym can have multiple references, each optionally with link
        for ref in sel.xpath('span[@class="synonym_ref"]'):
            refname = ref.xpath('normalize-space(string())')
            references.append({
                'name': refname.extract()[0][1:-1],
                'URI': ''
                })
        for ref in sel.xpath('a[@class="synonym_ref"]'):
            references.append({
                'name': ref.xpath('@title').extract()[0],
                'URI': ref.xpath('@href').extract()[0]
                })
        for ref in references:
            log.msg('CS synonym ref: %s %s' % (ref['name'], ref['URI']),
                    level=log.DEBUG)
        synonym = {
            'name': name,
            'category': category,
            'language': language,
            'references': references
            }
        return synonym

    def parse_extendedinfo(self, response):
        """Scrape data from the ChemSpider GetExtendedCompoundInfo API"""
        sel = Selector(response)
        properties = []
        names = sel.xpath('*').xpath('name()').extract()
        values = sel.xpath('*').xpath('text()').extract()
        for (name, value) in zip(names,values):
            result = Result({
                'attribute': name,
                'value': value, #These values have no unit!
                'source': 'ChemSpider ExtendedCompoundInfo',
                'reliability': 'Unknown',
                'conditions': ''
                })
            properties.append(result)
        return properties

    def parse_searchrequest(self, response):
        """Parse the initial response of the ChemSpider Search API """
        sel = Selector(response)
        log.msg('chemspider parse_searchrequest', level=log.DEBUG)
        sel.register_namespace('cs', 'http://www.chemspider.com/')
        csid = sel.xpath('.//cs:int/text()').extract()[0]
        # [TODO] - handle multiple csids in case of vague search term
        structure_url = self.website[:-1] + self.structure % csid
        extendedinfo_url = self.website[:-1] + self.extendedinfo % csid
        log.msg('chemspider URL: %s' % structure_url, level=log.DEBUG)
        return [Request(url=structure_url,
                        callback=self.parse),
                Request(url=extendedinfo_url,
                        callback=self.parse_extendedinfo)]

    def new_compound_request(self,compound):
        if compound in self.ignore_list: #[TODO] - add regular expression
            return None
        searchurl = self.website[:-1] + self.search % compound
        log.msg('chemspider compound', level=log.DEBUG)
        return Request(url=searchurl, callback=self.parse_searchrequest)