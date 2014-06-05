#!/usr/bin/env python
"""
Fourmi, a web scraper build to search specific information for a given compound (and it's pseudonyms).

Usage:
    fourmi search <compound>
    fourmi [options] search <compound>
    fourmi [options] [--include=<sourcename> | --exclude=<sourcename>] search <compound>
    fourmi list
    fourmi [--include=<sourcename> | --exclude=<sourcename>] list
    fourmi -h | --help
    fourmi --version

Options:
    --attributes=<regex>            Include only that match these regular expressions split by a comma. [default: .*]
    -h --help                       Show this screen.
    --version                       Show version.
    --verbose                       Verbose logging output.
    --log=<file>                    Save log to an file.
    -o <file> --output=<file>       Output file [default: result.*format*]
    -f <format> --format=<format>   Output formats (supported: csv, json, jsonlines, xml) [default: jsonlines]
    --include=<regex>               Include only sources that match these regular expressions split by a comma.
    --exclude=<regex>               Exclude the sources that match these regular expressions split by a comma.
"""

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
import docopt

from FourmiCrawler.spider import FourmiSpider
from sourceloader import SourceLoader


def setup_crawler(compound, settings, source_loader, attributes):
    """
    This function prepares and start the crawler which starts the actual search on the internet
    :param compound: The compound which should be searched
    :param settings: A scrapy settings object
    :param source_loader: A fully functional SourceLoader object which contains only the sources that should be used.
    :param attributes: A list of regular expressions which the attribute names should match.
    """
    spider = FourmiSpider(compound=compound, selected_attributes=attributes)
    spider.add_sources(source_loader.sources)
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()


def scrapy_settings_manipulation(docopt_arguments):
    """
    This function manipulates the Scrapy settings that normally would be set in the settings file. In the Fourmi
    project these are command line arguments.
    :param docopt_arguments: A dictionary generated by docopt containing all CLI arguments.
    """
    settings = get_project_settings()

    if docopt_arguments["--output"] != 'result.*format*':
        settings.overrides["FEED_URI"] = docopt_arguments["--output"]
    elif docopt_arguments["--format"] == "jsonlines":
        settings.overrides["FEED_URI"] = "results.json"
    elif docopt_arguments["--format"] is not None:
        settings.overrides["FEED_URI"] = "results." + docopt_arguments["--format"]

    if docopt_arguments["--format"] is not None:
        settings.overrides["FEED_FORMAT"] = docopt_arguments["--format"]

    return settings


def start_log(docopt_arguments):
    """
    This function starts the logging functionality of Scrapy using the settings given by the CLI.
    :param docopt_arguments:  A dictionary generated by docopt containing all CLI arguments.
    """
    if docopt_arguments["--log"] is not None:
        if docopt_arguments["--verbose"]:
            log.start(logfile=docopt_arguments["--log"], logstdout=False, loglevel=log.DEBUG)
        else:
            log.start(logfile=docopt_arguments["--log"], logstdout=True, loglevel=log.WARNING)
    else:
        if docopt_arguments["--verbose"]:
            log.start(logstdout=False, loglevel=log.DEBUG)
        else:
            log.start(logstdout=True, loglevel=log.WARNING)


def search(docopt_arguments, source_loader):
    """
    The function that facilitates the search for a specific compound.
    :param docopt_arguments: A dictionary generated by docopt containing all CLI arguments.
    :param source_loader: An initiated SourceLoader object pointed at the directory with the sources.
    """
    start_log(docopt_arguments)
    settings = scrapy_settings_manipulation(docopt_arguments)
    setup_crawler(docopt_arguments["<compound>"], settings, source_loader, docopt_arguments["--attributes"].split(','))
    reactor.run()


# The start for the Fourmi Command Line interface.
if __name__ == '__main__':
    arguments = docopt.docopt(__doc__, version='Fourmi - V0.4.2')
    loader = SourceLoader()

    if arguments["--include"]:
        loader.include(arguments["--include"].split(','))
    elif arguments["--exclude"]:
        loader.exclude(arguments["--exclude"].split(','))

    if arguments["search"]:
        search(arguments, loader)
    elif arguments["list"]:
        print "-== Available Sources ==-"
        print str(loader)
