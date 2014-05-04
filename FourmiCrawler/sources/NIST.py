from source import Source
from scrapy import log
from scrapy.http import Request
from scrapy.selector import Selector
from FourmiCrawler.items import Result


class NIST(Source):
    website = "http://webbook.nist.gov/*"  

    search = 'cgi/cbook.cgi?Name=%s&Units=SI&cTG=on&cTC=on&cTP=on'

    def __init__(self):
        Source.__init__(self)

    def parse(self, response):
        sel = Selector(response)

        symbol_table = {}
        tds = sel.xpath('//table[@class="symbol_table"]/tr/td')
        for (symbol_td, name_td) in zip(tds[::2], tds[1::2]):
            symbol = ''.join(symbol_td.xpath('node()').extract())
            name = name_td.xpath('text()').extract()[0]
            symbol_table[symbol] = name
            log.msg('NIST symbol: |%s|, name: |%s|' % (symbol, name),
                    level=log.DEBUG)

    def new_compound_request(self, compound):
        return Request(url=self.website[:-1] + self.search % compound,
                       callback=self.parse)
