from scrapy import log
# from scrapy.http import Request


class Source:
    website = "http://something/*"  # Regex of URI's the source is able to parse
    _spider = None

    def __init__(self):
        pass

    def parse(self, reponse):
        log.msg("The parse function of the empty parser was used.", level=log.WARNING)
        pass

    def new_compound_request(self, compound):
        # return Request(url=self.website[:-1] + compound, callback=self.parse)
        pass

    def set_spider(self, spider):
        self._spider = spider
