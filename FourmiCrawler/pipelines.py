# For more information on item pipelines, see the Scrapy documentation in:
# http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

from scrapy.exceptions import DropItem

class RemoveNonePipeline(object):

    def __init__(self):
        self.known_values = set()

    def process_item(self, item, spider):
        """
        Processing the items so None values are replaced by empty strings
        :param item: The incoming item
        :param spider: The spider which scraped the spider
        :return: :raise DropItem: Returns the item if unique or drops them if it's already known
        """
        for key in item:
            if item[key] is None:
                item[key] = ""
        return item

class DuplicatePipeline(object):

    def __init__(self):
        self.known_values = set()

    def process_item(self, item, spider):
        """
        Processing the items so exact doubles are dropped
        :param item: The incoming item
        :param spider: The spider which scraped the spider
        :return: :raise DropItem: Returns the item if unique or drops them if it's already known
        """
        value = (item['attribute'], item['value'], item['conditions'])
        if value in self.known_values:
            raise DropItem("Duplicate item found: %s" % item) # #[todo] append sources of first item.
        else:
            self.known_values.add(value)
            return item

class AttributeSelectionPipeline(object):

    def __init__(self):
        pass;

    def process_item(self, item, spider):
        """
        The items are processed using the selected attribute list available in the spider,
        items that don't match the selected items are dropped.
        :param item: The incoming item
        :param spider: The spider which scraped the item. Should have an attribute "selected_attributes".
        :return: :raise DropItem: Returns item if it matches an selected attribute, else it is dropped.
        """
        if [x for x in spider.selected_attributes if re.match(x, item["attribute"])]:
            return item
        else:
            raise DropItem("Attribute not selected by used: %s" % item)