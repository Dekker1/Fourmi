from scrapy import log
# from scrapy.http import Request


class Parser:
	'''
	website should be an regular expression of the urls of request the parser is able to parse.
	'''
	website = "http://something/*"
	__spider = None

	def parse(self, reponse):
		log.msg("The parse function of the empty parser was used.", level=log.WARNING)
		pass

	def new_compound_request(self, compound):
		# return Request(url=self.website[:-1] + compound, callable=self.parse)
		pass

	def set_spider(self, spider):
		self.__spider = spider
