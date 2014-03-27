#!/usr/bin/env python
"""
Fourmi - An internet webcrawler searching for information on chemical compounds.
[todo] - Add some more useful text here.
"""

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from FourmiCrawler.spiders.Fourmispider import FourmiSpider
from scrapy.utils.project import get_project_settings

def setup_crawler(searchable):
  spider = FourmiSpider(compound=searchable) # [todo] - Do something smart to get the different spiders to work here.
  settings = get_project_settings()
  crawler = Crawler(settings)
  crawler.configure()
  crawler.crawl(spider)
  crawler.start()

def start():
  setup_crawler("Methane")
  log.start()
  reactor.run()

start()
