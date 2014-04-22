#!/usr/bin/env python
"""
Fourmi, a web scraper build to search specific information for a given compound (and it's pseudonyms).

Usage:
    fourmi search <compound>
    fourmi [options] search <compound>
    fourmi list
    fourmi -h | --help
    fourmi --version

Options:
    -h --help                       Show this screen.
    --version                       Show version.
    --verbose                       Verbose logging output.
    --log=<file>                    Save log to an file.
    -o <file> --output=<file>       Output file [default: result.*format*]
    -f <format> --format=<format>   Output formats (supported: csv, json, jsonlines, xml) [default: jsonlines]
    --include=<sourcenames>         Include only sources that match the regular these expressions split by a comma.
    --exclude=<sourcenames>         Exclude the sources that match the regular these expressions split by a comma.
"""

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
import docopt

from FourmiCrawler.spider import FourmiSpider
from sourceloader import SourceLoader


def setup_crawler(searchable, settings, loader):
    spider = FourmiSpider(compound=searchable)
    spider.add_parsers(loader.sources)
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()


def scrapy_settings_manipulation(arguments):
    settings = get_project_settings()

    if arguments["--output"] != 'result.*format*':
        settings.overrides["FEED_URI"] = arguments["--output"]
    elif arguments["--format"] == "jsonlines":
        settings.overrides["FEED_URI"] = "results.json"
    elif arguments["--format"] is not None:
        settings.overrides["FEED_URI"] = "results." + arguments["--format"]

    if arguments["--format"] is not None:
        settings.overrides["FEED_FORMAT"] = arguments["--format"]

    return settings


def start_log(arguments):
    if arguments["--log"] is not None:
        if arguments["--verbose"]:
            log.start(logfile=arguments["--log"], logstdout=False, loglevel=log.DEBUG)
        else:
            log.start(logfile=arguments["--log"], logstdout=True, loglevel=log.WARNING)
    else:
        if arguments["--verbose"]:
            log.start(logstdout=False, loglevel=log.DEBUG)
        else:
            log.start(logstdout=True, loglevel=log.WARNING)


def search(arguments, loader):
    start_log(arguments)
    settings = scrapy_settings_manipulation(arguments)
    setup_crawler(arguments["<compound>"], settings, loader)
    reactor.run()


if __name__ == '__main__':
    arguments = docopt.docopt(__doc__, version='Fourmi - V0.1.0')
    loader = SourceLoader()

    if arguments["search"]:
        search(arguments, loader)
    elif arguments["list"]:
        print "-== Available Sources ==-"
        print str(loader)
