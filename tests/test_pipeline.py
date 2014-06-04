import copy
import unittest

from scrapy.exceptions import DropItem

from FourmiCrawler import pipelines, spider, items


class TestPipelines(unittest.TestCase):
    def setUp(self):
        self.testItem = items.Result()

    def test_none_pipeline(self):
        # Testing the pipeline that replaces the None values in items.
        self.testItem["value"] = "abc"
        pipe = pipelines.RemoveNonePipeline()
        processed = pipe.process_item(self.testItem, spider.FourmiSpider())

        self.assertTrue(processed["value"] == "abc")

        for key in self.testItem:
            self.assertIsNotNone(processed[key])
            if key is not "value":
                self.assertIs(processed[key], "")

    def test_duplicate_pipeline(self):
        # Testing the pipeline that removes duplicates.
        self.testItem["attribute"] = "test"
        self.testItem["value"] = "test"
        self.testItem["conditions"] = "test"

        pipe = pipelines.DuplicatePipeline()
        self.assertEqual(pipe.process_item(self.testItem, spider.FourmiSpider()), self.testItem)
        self.assertRaises(DropItem, pipe.process_item, self.testItem, spider.FourmiSpider())

        other_item = copy.deepcopy(self.testItem)
        other_item["value"] = "test1"
        self.assertEqual(pipe.process_item(other_item, spider.FourmiSpider()), other_item)

    def test_attribute_selection(self):
        # Testing the pipeline that selects attributes.
        item1 = copy.deepcopy(self.testItem)
        item2 = copy.deepcopy(self.testItem)

        item1["attribute"] = "abd"
        item2["attribute"] = "abc"

        s = spider.FourmiSpider(selected_attributes=["a.d"])
        pipe = pipelines.AttributeSelectionPipeline()

        self.assertEqual(pipe.process_item(item1, s), item1)
        self.assertRaises(DropItem, pipe.process_item, item2, s)