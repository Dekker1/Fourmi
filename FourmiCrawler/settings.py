# Scrapy settings for Fourmi project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
# http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'FourmiCrawler'

SPIDER_MODULES = ['FourmiCrawler']
NEWSPIDER_MODULE = 'FourmiCrawler'
ITEM_PIPELINES = {
    "FourmiCrawler.pipelines.RemoveNonePipeline": 100,
    'FourmiCrawler.pipelines.AttributeSelectionPipeline': 200,
    'FourmiCrawler.pipelines.DuplicatePipeline': 300,
}
FEED_URI = 'results.json'
FEED_FORMAT = 'jsonlines'

# Crawl responsibly by identifying yourself (and your website) on the
# user-agent

# [todo] - Check for repercussions on spoofing the user agent

USER_AGENT = 'Fourmi'
# USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36'
