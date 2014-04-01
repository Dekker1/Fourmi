from scrapy.spider import Spider
from scrapy import log
import re


class FourmiSpider(Spider):
	name = "FourmiSpider"
	__parsers = []

	def __init__(self, compound=None, *args, **kwargs):
		super(FourmiSpider, self).__init__(*args, **kwargs)
		self.synonyms = [compound]

	def parse(self, reponse):
		for parser in self.parsers:
			if re.match(parser.website, reponse.url):
				log.msg("Url: " + reponse.url + " -> Parser: " + parser.website, level=log.DEBUG)
				return parser.parse(reponse)
		return None

	def get_synonym_requests(self, compound):
		requests = []
		for parser in self.parsers:
			requests.append(parser.new_compound_request(compound))
		return requests


	def add_parsers(self, parsers):
		for parser in parsers:
			self.add_parser(parser)

	def add_parser(self, parser):
		self.__parsers.add(parser)
		parser.set_spider(self)