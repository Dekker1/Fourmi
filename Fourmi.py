#!/usr/bin/env python
"""
Fourmi - An internet webcrawler searching for information on chemical compounds.
[todo] - Add some more useful text here.
"""

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from FourmiCrawler.spiders.Chemspider import ChemspiderSpider # [review] - There should be an easy way to import all spiders!
from scrapy.utils.project import get_project_settings

# [todo] - Add something to add all spiders, with the right references
spider = ChemspiderSpider(compound = "Aspirin")
settings = get_project_settings()
crawler = Crawler(settings)
crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
crawler.configure()
crawler.crawl(spider)
crawler.start()
log.start()
reactor.run()