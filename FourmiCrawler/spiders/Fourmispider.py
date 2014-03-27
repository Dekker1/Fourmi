from scrapy.spider import Spider

class FourmiSpider(Spider):
  name="FourmiSpider"

  def __init__(self, compound=None, *args, **kwargs):
    super(FourmiSpider, self).__init__(*args, **kwargs)
    # [TODO] - Initiate all parsers for the different websites and get allowed URLs.
        
  def parse(self, reponse):
    # [TODO] - This function should delegate it's functionality to other parsers.
    pass
