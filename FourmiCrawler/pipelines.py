# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem


class FourmiPipeline(object):

    def __init__(self):
        self.known_values = set()

    def process_item(self, item, spider):
        """
        Processing the items so exact doubles are dropped
        :param item: The incoming item
        :param spider: The spider which scraped the spider
        :return: :raise DropItem: Returns the item if unique or drops them if it's already known
        """
        value = item['attribute'], item['value']
        if value in self.known_values:
            raise DropItem("Duplicate item found: %s" % item) # #[todo] append sources of first item.
        else:
            self.known_values.add(value)
            return item
