from scrapy import log


class Parser:
    website = "http://localhost/*"

    def parse(self, reponse):
        log.msg("The parse function of the empty parser was used.", level=log.Warning)
        pass
