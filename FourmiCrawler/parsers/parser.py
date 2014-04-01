from scrapy import log


class Parser:
	'''
	website should be an regular expression of websites you want to parse.
	'''
	website = "http://something/*"
	__spider = None

	def parse(self, reponse):
		log.msg("The parse function of the empty parser was used.", level=log.WARNING)
		pass

	def generate_search_url(self, compound):
	 	# return website[:-1] + compound
		pass

	def set_spider(self, spider):
		self.__spider = spider
