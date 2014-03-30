from scrapy.spider import Spider


class FourmiSpider(Spider):
	name = "FourmiSpider"

	def __init__(self, compound=None, *args, **kwargs):
		super(FourmiSpider, self).__init__(*args, **kwargs)
		self.synonyms = [compound]


def parse(self, reponse):
	# [TODO] - This function should delegate it's functionality to other
	# parsers.
	pass


def add_parser(self, parser):
	self.parsers.add(parser)
