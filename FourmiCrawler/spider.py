import re

from scrapy.spider import Spider
from scrapy import log


class FourmiSpider(Spider):
    """
    A spider writen for the Fourmi Project which calls upon all available sources to request and scrape data.
    """
    name = "FourmiSpider"

    def __init__(self, compound=None, selected_attributes=None, *args, **kwargs):
        """
        Initiation of the Spider
        :param compound: compound that will be searched.
        :param selected_attributes: A list of regular expressions that the attributes should match.
        """
        self._sources = []
        self.synonyms = set()
        super(FourmiSpider, self).__init__(*args, **kwargs)
        self.synonyms.add(compound)
        if selected_attributes is None:
            self.selected_attributes = [".*"]
        else:
            self.selected_attributes = selected_attributes

    def parse(self, response):
        """
        The function that is called when a response to a request is available. This function distributes this to a
        source which should be able to handle parsing the data.
        :param response: A Scrapy Response object that should be parsed
        :return: A list of Result items and new Request to be handled by the scrapy core.
        """
        for source in self._sources:
            if re.match(source.website, response.url):
                log.msg("Url: " + response.url + " -> Source: " + source.website, level=log.DEBUG)
                return source.parse(response)
        return None

    def get_synonym_requests(self, compound, force=False):
        """
        A function that generates new Scrapy Request for each source given a new synonym of a compound.
        :param compound: A compound name
        :return: A list of Scrapy Request objects
        """
        requests = []
        if force or compound not in self.synonyms:
            self.synonyms.add(compound)
            for parser in self._sources:
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
            requests.extend(self.get_synonym_requests(synonym, force=True))
        return requests

    def add_sources(self, sources):
        """
        A function to add a new Parser objects to the list of available sources.
        :param sources: A list of Source Objects.
        """
        for parser in sources:
            self.add_source(parser)

    def add_source(self, source):
        """
        A function add a new Parser object to the list of available parsers.
        :param source: A Source Object
        """
        self._sources.append(source)
        source.set_spider(self)