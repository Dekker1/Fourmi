from scrapy import log
# from scrapy.http import Request


class NIST(Source):
    website = "http://webbook.nist.gov/*"  

    def __init__(self):
        Source.__init__(self)

    def parse(self, reponse):
        pass

    def new_compound_request(self, compound):
        # return Request(url=self.website[:-1] + compound, callback=self.parse)
        pass
