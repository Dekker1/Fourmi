#!/usr/bin/env python
"""
Fourmi, an webscraper build to search specific information for a given compound.

Usage:
    fourmi search <compound>
    fourmi [options] search <compound>
    fourmi -h | --help
    fourmi --version

Options:
    -h --help       Show this screen.
    --version       Show version.
    --verbose       Verbose logging output.
    --log=<file>    Save log to an file.
"""

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from FourmiCrawler.parsers.parser import Parser
from FourmiCrawler.spider import FourmiSpider
from scrapy.utils.project import get_project_settings
import os, inspect
import docopt


def load_parsers(rel_dir="FourmiCrawler/parsers"):
    path = os.path.dirname(os.path.abspath(__file__))
    path += "/" + rel_dir
    parsers = []
    known_parser = set()

    for py in [f[:-3] for f in os.listdir(path) if f.endswith('.py') and f != '__init__.py']:
        mod = __import__('.'.join([rel_dir.replace("/", "."), py]), fromlist=[py])
        classes = [getattr(mod, x) for x in dir(mod) if inspect.isclass(getattr(mod, x))]
        for cls in classes:
            if issubclass(cls, Parser) and cls not in known_parser:
                parsers.append(cls()) # [review] - Would we ever need arguments for the parsers?
                known_parser.add(cls)
    return parsers

def setup_crawler(searchables):
    spider = FourmiSpider(compounds=searchables)
    spider.add_parsers(load_parsers())
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()


def start():
    setup_crawler(["Methane"])
    log.start()
    reactor.run()


start()
