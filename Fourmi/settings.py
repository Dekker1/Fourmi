# Scrapy settings for Fourmi project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'Fourmi'

SPIDER_MODULES = ['Fourmi.spiders']
NEWSPIDER_MODULE = 'Fourmi.spiders'
ITEM_PIPELINES = {
    'Fourmi.pipelines.FourmiPipeline': 100
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Fourmi (+http://www.yourdomain.com)'
