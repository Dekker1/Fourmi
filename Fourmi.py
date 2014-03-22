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

defined_spiders = [ChemspiderSpider(compound = "Methane")]

def setup_crawler(Spider, compound):
  spider = FollowAllSpider(domain=domain) # [todo] - Do something smart to get the different spiders to work here.
  settings = get_project_settings()
  crawler = Crawler(settings)
  crawler.configure()
  crawler.crawl(spider)
  crawler.start()

def start():
  for spider in defined_spiders:
    setup_crawler(spider, compound)
  log.start()
  reactor.run()

start()
