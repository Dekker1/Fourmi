import re

from scrapy.spider import Spider
from scrapy import log


class FourmiSpider(Spider):
    """
    A spider writen for the Fourmi Project which calls upon all available sources to request and scrape data.
    """
    name = "FourmiSpider"
    __parsers = []
    synonyms = []

    def __init__(self, compound=None, selected_attributes=[".*"], *args, **kwargs):
        """
        Initiation of the Spider
        :param compound: compound that will be searched.
        :param selected_attributes: A list of regular expressions that the attributes should match.
        """
        super(FourmiSpider, self).__init__(*args, **kwargs)
        self.synonyms.append(compound)
        self.selected_attributes = selected_attributes;

    def parse(self, reponse):
        """
        The function that is called when a response to a request is available. This function distributes this to a
        parser which should be able to handle parsing the data.
        :param reponse: A Scrapy Response object that should be parsed
        :return: A list of Result items and new Request to be handled by the scrapy core.
        """
        for parser in self.__parsers:
            if re.match(parser.website, reponse.url):
                log.msg("Url: " + reponse.url + " -> Source: " + parser.website, level=log.DEBUG)
                return parser.parse(reponse)
        return None

    def get_synonym_requests(self, compound):
        """
        A function that generates new Scrapy Request for each source given a new synonym of a compound.
        :param compound: A compound name
        :return: A list of Scrapy Request objects
        """
        requests = []
        for parser in self.__parsers:
            parser_requests = parser.new_compound_request(compound)
            if parser_requests is not None:
                requests.append(parser_requests)
        return requests

    def start_requests(self):
        """
        The function called by Scrapy for it's first Requests
        :return: A list of Scrapy Request generated from the known synonyms using the available sources.
        """
        requests = []
        for synonym in self.synonyms:
            requests.extend(self.get_synonym_requests(synonym))
        return requests

    def add_parsers(self, parsers):
        """
        A function to add a new Parser objects to the list of available parsers.
        :param parsers: A list of Parser Objects.
        """
        for parser in parsers:
            self.add_parser(parser)

    def add_parser(self, parser):
        """
        A function add a new Parser object to the list of available parsers.
        :param parser: A Parser Object
        """
        self.__parsers.append(parser)
        parser.set_spider(self)