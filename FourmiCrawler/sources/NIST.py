from source import Source
from scrapy import log
from scrapy.http import Request
from scrapy.selector import Selector
from FourmiCrawler.items import Result
import re

# [TODO]: values can be '128.', perhaps remove the dot in that case?
# [TODO]: properties have references and comments which do not exist in the
#         Result item, but should be included eventually.

class NIST(Source):
    """NIST Scraper plugin

    This plugin manages searching for a chemical on the NIST website
    and parsing the resulting page if the chemical exists on NIST.
    """
    website = "http://webbook.nist.gov/*"  

    search = 'cgi/cbook.cgi?Name=%s&Units=SI&cTP=on'

    ignore_list = set()

    def __init__(self):
        Source.__init__(self)

    def parse(self, response):
        sel = Selector(response)

        title = sel.xpath('head/title/text()').extract()[0]
        if title == 'Name Not Found':
            log.msg('NIST: Chemical not found!', level=log.ERROR)
            return
        if title not in self.ignore_list:
            self.ignore_list.update(title)
            log.msg('NIST emit synonym: %s' % title, level=log.DEBUG)
            self._spider.get_synonym_requests(title)

        requests = []

        requests.extend(self.parse_generic_info(sel))

        symbol_table = {}
        tds = sel.xpath('//table[@class="symbol_table"]/tr/td')
        for (symbol_td, name_td) in zip(tds[::2], tds[1::2]):
            symbol = ''.join(symbol_td.xpath('node()').extract())
            name = name_td.xpath('text()').extract()[0]
            symbol_table[symbol] = name
            log.msg('NIST symbol: |%s|, name: |%s|' % (symbol, name),
                    level=log.DEBUG)

        for table in sel.xpath('//table[@class="data"]'):
            summary = table.xpath('@summary').extract()[0]
            if summary == 'One dimensional data':
                log.msg('NIST table: Aggregrate data', level=log.DEBUG)
                requests.extend(
                    self.parse_aggregate_data(table, symbol_table))
            elif table.xpath('tr/th="Initial Phase"').extract()[0] == '1':
                log.msg('NIST table; Enthalpy/entropy of phase transition',
                        level=log.DEBUG)
                requests.extend(self.parse_transition_data(table, summary))
            elif table.xpath('tr[1]/td'):
                log.msg('NIST table: Horizontal table', level=log.DEBUG)
            elif summary == 'Antoine Equation Parameters':
                log.msg('NIST table: Antoine Equation Parameters',
                        level=log.DEBUG)
                requests.extend(self.parse_antoine_data(table, summary))
            elif len(table.xpath('tr[1]/th')) == 5:
                log.msg('NIST table: generic 5 columns', level=log.DEBUG)
                # Symbol (unit) Temperature (K) Method Reference Comment
                requests.extend(self.parse_generic_data(table, summary))
            elif len(table.xpath('tr[1]/th')) == 4:
                log.msg('NIST table: generic 4 columns', level=log.DEBUG)
                # Symbol (unit) Temperature (K) Reference Comment
                requests.extend(self.parse_generic_data(table, summary))
            else:
                log.msg('NIST table: NOT SUPPORTED', level=log.WARNING)
                continue #Assume unsupported
        return requests

    def parse_generic_info(self, sel):
        """Parses: synonyms, chemical formula, molecular weight, InChI,
        InChiKey, CAS number
        """
        ul = sel.xpath('body/ul[li/strong="IUPAC Standard InChI:"]')
        li = ul.xpath('li')

        raw_synonyms = ul.xpath('li[strong="Other names:"]/text()').extract()
        for synonym in raw_synonyms[0].strip().split(';\n'):
            log.msg('NIST synonym: %s' % synonym, level=log.DEBUG)
            self.ignore_list.update(synonym)
            self._spider.get_synonym_requests(synonym)

        data = {}

        raw_formula = ul.xpath('li[strong/a="Formula"]//text()').extract()
        data['Chemical formula'] = ''.join(raw_formula[2:]).strip()

        raw_mol_weight = ul.xpath('li[strong/a="Molecular weight"]/text()')
        data['Molecular weight'] = raw_mol_weight.extract()[0].strip()

        raw_inchi = ul.xpath('li[strong="IUPAC Standard InChI:"]//tt/text()')
        data['IUPAC Standard InChI'] = raw_inchi.extract()[0]

        raw_inchikey = ul.xpath('li[strong="IUPAC Standard InChIKey:"]'
                            '/tt/text()')
        data['IUPAC Standard InChIKey'] = raw_inchikey.extract()[0]

        raw_cas_number = ul.xpath('li[strong="CAS Registry Number:"]/text()')
        data['CAS Registry Number'] = raw_cas_number.extract()[0].strip()

        requests = []
        for key, value in data.iteritems():
            result = Result({
                'attribute': key,
                'value': value,
                'source': 'NIST',
                'reliability': 'Unknown',
                'conditions': ''
            })
            requests.append(result)

        return requests

    def parse_aggregate_data(self, table, symbol_table):
        """Parses the table(s) which contain possible links to individual
        data points
        """
        results = []
        for tr in table.xpath('tr[td]'):
            extra_data_url = tr.xpath('td[last()][a="Individual data points"]'
                                '/a/@href').extract()
            if extra_data_url:
                request = Request(url=self.website[:-1] + extra_data_url[0],
                    callback=self.parse_individual_datapoints)
                results.append(request)
                continue
            data = []
            for td in tr.xpath('td'):
                data.append(''.join(td.xpath('node()').extract()))

            name = symbol_table[data[0]]
            condition = ''

            m = re.match(r'(.*) at (.*)', name)
            if m:
                name = m.group(1)
                condition = m.group(2)

            result = Result({
                'attribute': name,
                'value': data[1] + ' ' + data[2],
                'source': 'NIST',
                'reliability': 'Unknown',
                'conditions': condition
            })
            log.msg('NIST: |%s|' % data, level=log.DEBUG)
            results.append(result)
        return results

    @staticmethod
    def parse_transition_data(table, summary):
        """Parses the table containing properties regarding phase changes"""
        results = []

        name = table.xpath('@summary').extract()[0]
        tr_unit = ''.join(table.xpath('tr[1]/th[1]/node()').extract())
        m = re.search(r'\((.*)\)', tr_unit)
        unit = '!'
        if m:
            unit = m.group(1)

        for tr in table.xpath('tr[td]'):
            tds = tr.xpath('td/text()').extract()
            result = Result({
                'attribute': name,
                'value': tds[0] + ' ' + unit,
                'source': 'NIST',
                'reliability': 'Unknown',
                'conditions': '%s K, (%s -> %s)' % (tds[1], tds[2], tds[3])
            })
            results.append(result)


        return results

    @staticmethod
    def parse_generic_data(table, summary):
        """Parses the common tables of 4 and 5 rows. Assumes they are of the
        form:
        Symbol (unit)|Temperature (K)|Method|Reference|Comment
        Symbol (unit)|Temperature (K)|Reference|Comment
        """
        results = []

        name = table.xpath('@summary').extract()[0]
        tr_unit = ''.join(table.xpath('tr[1]/th[1]/node()').extract())
        m = re.search(r'\((.*)\)', tr_unit)
        unit = '!'
        if m:
            unit = m.group(1)

        for tr in table.xpath('tr[td]'):
            tds = tr.xpath('td/text()').extract()
            result = Result({
                'attribute': name,
                'value': tds[0] + ' ' + unit,
                'source': 'NIST',
                'reliability': 'Unknown',
                'conditions': '%s K' % tds[1]
            })
            results.append(result)
        return results

    @staticmethod
    def parse_antoine_data(table, summary):
        """Parse table containing parameters for the Antione equation"""
        results = []

        name = table.xpath('@summary').extract()[0]

        for tr in table.xpath('tr[td]'):
            tds = tr.xpath('td/text()').extract()
            result = Result({
                'attribute': name,
                'value': 'A=%s, B=%s, C=%s' % (tds[1], tds[2], tds[3]),
                'source': 'NIST',
                'reliability': 'Unknown',
                'conditions': '%s K' % tds[0]
            })
            results.append(result)

        return results

    def parse_individual_datapoints(self, response):
        """Parses the page linked from aggregate data"""
        sel = Selector(response)
        table = sel.xpath('//table[@class="data"]')[0]

        results = []

        name = table.xpath('@summary').extract()[0]
        condition = ''
        m = re.match(r'(.*) at (.*)', name)
        if m:
            name = m.group(1)
            condition = m.group(2)

        tr_unit = ''.join(table.xpath('tr[1]/th[1]/node()').extract())
        m = re.search(r'\((.*)\)', tr_unit)
        unit = '!'
        if m:
            unit = m.group(1)

        for tr in table.xpath('tr[td]'):
            tds = tr.xpath('td/text()').extract()
            uncertainty = ''
            m = re.search('Uncertainty assigned by TRC =  (.*?) ', tds[-1])
            if m:
                uncertainty = '+- %s ' % m.group(1)
                # [TODO]: get the plusminus sign working in here
            result = Result({
                'attribute': name,
                'value': '%s %s%s' % (tds[0], uncertainty, unit),
                'source': 'NIST',
                'reliability': 'Unknown',
                'conditions': condition
            })
            results.append(result)

        return results

    def new_compound_request(self, compound):
        if compound not in self.ignore_list:
            self.ignore_list.update(compound)
            return Request(url=self.website[:-1] + self.search % compound,
                           callback=self.parse)
