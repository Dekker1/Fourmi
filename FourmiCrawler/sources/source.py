from scrapy import log
# from scrapy.http import Request


class Source:
    website = "http://something/.*"  # Regex of URI's the source is able to parse
    _spider = None

    def __init__(self, config=None):
        """
        Initiation of a new Source
        """
        self.cfg = {}
        if config is not None:
            self.cfg = config
        pass

    def parse(self, response):
        """
        This function should be able to parse all Scrapy Response objects with a URL matching the website Regex.
        :param response: A Scrapy Response object
        :return: A list of Result items and new Scrapy Requests
        """
        log.msg("The parse function of the empty source was used.", level=log.WARNING)
        pass

    def new_compound_request(self, compound):
        """
        This function should return a Scrapy Request for the given compound request.
        :param compound: A compound name.
        :return: A new Scrapy Request
        """
        # return Request(url=self.website[:-2] + compound, callback=self.parse)
        pass

    def set_spider(self, spider):
        """
        A Function to save the associated spider.
        :param spider: A FourmiSpider object
        """
        self._spider = spider
