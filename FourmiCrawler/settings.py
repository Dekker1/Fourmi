# Scrapy settings for Fourmi project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'FourmiCrawler'

SPIDER_MODULES = ['FourmiCrawler']
NEWSPIDER_MODULE = 'FourmiCrawler'
ITEM_PIPELINES = {
    'FourmiCrawler.pipelines.FourmiPipeline': 100
}

# Crawl responsibly by identifying yourself (and your website) on the
# user-agent

# USER_AGENT = 'FourmiCrawler (+http://www.yourdomain.com)'
