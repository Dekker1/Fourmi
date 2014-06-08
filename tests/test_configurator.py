import unittest
from utils.configurator import Configurator


class TestConfigurator(unittest.TestCase):

    def setUp(self):
        self.conf = Configurator()

    def test_set_output(self):
        self.conf.set_output(filename="test.txt", fileformat="csv")
        self.assertEqual(self.conf.scrapy_settings["FEED_URI"], "test.txt")
        self.assertEqual(self.conf.scrapy_settings["FEED_FORMAT"], "csv")

        self.conf.set_output("results.*format*", "jsonlines")
        self.assertEqual(self.conf.scrapy_settings["FEED_URI"], "results.json")
        self.assertEqual(self.conf.scrapy_settings["FEED_FORMAT"], "jsonlines")

        self.conf.set_output("results.*format*", "csv")
        self.assertEqual(self.conf.scrapy_settings["FEED_URI"], "results.csv")
        self.assertEqual(self.conf.scrapy_settings["FEED_FORMAT"], "csv")

    # def test_start_log(self):
    #     self.conf.start_log("test.log", True)
    #     self.conf.start_log("test.log", False)
    #     self.conf.start_log(None, True)
    #     self.conf.start_log(None, False)