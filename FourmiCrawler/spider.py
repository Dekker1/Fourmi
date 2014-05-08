from scrapy.spider import Spider
from scrapy import log
import re


class FourmiSpider(Spider):
    name = "FourmiSpider"
    __parsers = []
    synonyms = []

    def __init__(self, compound=None, selected_attributes=[".*"], *args, **kwargs):
        super(FourmiSpider, self).__init__(*args, **kwargs)
        self.synonyms.append(compound)
        self.selected_attributes = selected_attributes;

    def parse(self, reponse):
        for parser in self.__parsers:
            if re.match(parser.website, reponse.url):
                log.msg("Url: " + reponse.url + " -> Source: " + parser.website, level=log.DEBUG)
                return parser.parse(reponse)
        return None

    def get_synonym_requests(self, compound):
        requests = []
        for parser in self.__parsers:
            parser_requests = parser.new_compound_request(compound)
            if parser_requests is not None:
                requests.append(parser_requests)
        return requests

    def start_requests(self):
        requests = []
        for synonym in self.synonyms:
            requests.extend(self.get_synonym_requests(synonym))
        return requests

    def add_parsers(self, parsers):
        for parser in parsers:
            self.add_parser(parser)

    def add_parser(self, parser):
        self.__parsers.append(parser)
        parser.set_spider(self)