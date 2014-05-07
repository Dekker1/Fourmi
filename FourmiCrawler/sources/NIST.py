from source import Source
from scrapy import log
from scrapy.http import Request
from scrapy.selector import Selector
from FourmiCrawler.items import Result
import re

class NIST(Source):
    website = "http://webbook.nist.gov/*"  

    search = 'cgi/cbook.cgi?Name=%s&Units=SI&cTP=on'

    def __init__(self):
        Source.__init__(self)

    def parse(self, response):
        sel = Selector(response)

        requests = []

        symbol_table = {}
        tds = sel.xpath('//table[@class="symbol_table"]/tr/td')
        for (symbol_td, name_td) in zip(tds[::2], tds[1::2]):
            symbol = ''.join(symbol_td.xpath('node()').extract())
            name = name_td.xpath('text()').extract()[0]
            symbol_table[symbol] = name
            log.msg('NIST symbol: |%s|, name: |%s|' % (symbol, name),
                    level=log.DEBUG)

        for tables in sel.xpath('//table[@class="data"]'):
            if tables.xpath('@summary').extract()[0] == 'One dimensional data':
                log.msg('NIST table: Aggregrate data', level=log.DEBUG)
                requests.extend(
                    self.parse_aggregate_data(tables, symbol_table))
            elif tables.xpath('tr/th="Initial Phase"').extract()[0] == '1':
                log.msg('NIST table; Enthalpy/entropy of phase transition',
                        level=log.DEBUG)
                requests.extend(
                    self.parse_transition_data(tables, symbol_table))
            elif tables.xpath('tr[1]/td'):
                log.msg('NIST table: Horizontal table', level=log.DEBUG)
            elif (tables.xpath('@summary').extract()[0] ==
                    'Antoine Equation Parameters'):
                log.msg('NIST table: Antoine Equation Parameters',
                        level=log.DEBUG)
            elif len(tables.xpath('tr[1]/th')) == 5:
                log.msg('NIST table: generic 5 columns', level=log.DEBUG)
                # Symbol (unit) Temperature (K) Method Reference Comment
            elif len(tables.xpath('tr[1]/th')) == 4:
                log.msg('NIST table: generic 4 columns', level=log.DEBUG)
                # Symbol (unit) Temperature (K) Reference Comment
            else:
                log.msg('NIST table: NOT SUPPORTED', level=log.WARNING)
                continue #Assume unsupported
        return requests

    @staticmethod
    def parse_aggregate_data(table, symbol_table):
        results = []
        for tr in table.xpath('tr[td]'):
            data = []
            for td in tr.xpath('td'):
                data.append(''.join(td.xpath('node()').extract()))
            result = Result({
                'attribute': symbol_table[data[0]],
                'value': data[1] + ' ' + data[2],
                'source': 'NIST',
                'reliability': 'Unknown',
                'conditions': ''
            })
            log.msg('NIST: |%s|' % data, level=log.DEBUG)
            results.append(result)
        return results

    @staticmethod
    def parse_transition_data(table, symbol_table):
        results = []

        name = table.xpath('@summary').extract()[0]
        unit = table.xpath('tr[1]/th[1]/node()').extract()[-1][2:-1]

        for tr in table.xpath('tr[td]'):
            tds = tr.xpath('td/text()').extract()
            result = Result({
                'attribute': name,
                'value': tds[0] + ' ' + unit,
                'source': 'NIST',
                'reliability': 'Unknown',
                'conditions': '%s K, (%s -> %s)' % (tds[1], tds[2], tds[3])
            })
            log.msg('NIST: |%s|' % result, level=log.DEBUG)
            results.append(result)


        return results

    def new_compound_request(self, compound):
        return Request(url=self.website[:-1] + self.search % compound,
                       callback=self.parse)
