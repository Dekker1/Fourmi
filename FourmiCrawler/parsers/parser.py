from scrapy import log


class Parser:
	'''
	website should be an regular expression of websites you want to parse.
	'''
	website = "http://localhost/*"

	def parse(self, reponse):
		log.msg("The parse function of the empty parser was used.", level=log.WARNING)
		pass