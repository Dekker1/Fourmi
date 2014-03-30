#!/usr/bin/env python
"""
Fourmi - An internet webcrawler searching for information on chemical
compounds. [todo] - Add some more useful text here.
"""

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from FourmiCrawler.spider import FourmiSpider
from scrapy.utils.project import get_project_settings
from FourmiCrawler.parsers.parser import Parser


def setup_crawler(searchable):
	# [TODO] - Initiate all parsers for the different websites and get allowed URLs.
	spider = FourmiSpider(compound=searchable)
	spider.add_parser(Parser())
	settings = get_project_settings()
	crawler = Crawler(settings)
	crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
	crawler.configure()
	crawler.crawl(spider)
	crawler.start()


def start():
	setup_crawler("Methane")
	log.start()
	reactor.run()


start()
