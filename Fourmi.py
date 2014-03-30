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
import os, inspect

def load_parsers(rel_dir="FourmiCrawler/parsers"):
	path = os.path.dirname(os.path.abspath(__file__))
	path += "/" + rel_dir
	parsers = []

	for py in [f[:-3] for f in os.listdir(path) if f.endswith('.py') and f != '__init__.py']:
		mod = __import__('.'.join(["FourmiCrawler.parsers", py]), fromlist=[py]) # [todo] - This module name should be derived from the rel_dir variable
		classes = [getattr(mod, x) for x in dir(mod) if inspect.isclass(getattr(mod, x))]
		for cls in classes:
			parsers.append(cls()) # [review] - Would we ever need arguments for the parsers?
	return parsers

def setup_crawler(searchable):
	spider = FourmiSpider(compound=searchable)
	spider.add_parsers(load_parsers())
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
