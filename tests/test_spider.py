import unittest

from scrapy.http import Request

from FourmiCrawler import spider
from FourmiCrawler.sources.ChemSpider import ChemSpider
from FourmiCrawler.sources.source import Source


class TestFoumiSpider(unittest.TestCase):

    def setUp(self):
        self.compound = "test_compound"
        self.attributes = ["a.*", ".*a"]
        self.spi = spider.FourmiSpider(self.compound, self.attributes)

    def test_init(self):
        # Test the initiation of the Fourmi spider
        self.assertIn(self.compound, self.spi.synonyms)
        for attr in self.attributes:
            self.assertIn(attr, self.spi.selected_attributes)

    def test_add_source(self):
        # Testing the source adding function of the Fourmi spider
        src = Source()
        self.spi.add_source(src)
        self.assertIn(src, self.spi._sources)

    def test_add_sources(self):
        # Testing the function that adds multiple sources
        srcs = [Source(), Source(), Source()]
        self.spi.add_sources(srcs)

        for src in srcs:
            self.assertIn(src, self.spi._sources)

    def test_start_requests(self):
        # A test for the function that generates the start requests
        self.spi._sources = []

        src = Source()
        self.spi.add_source(src)
        self.assertEqual(self.spi.start_requests(), [])

        src2 = ChemSpider()
        self.spi.add_source(src2)
        self.assertIsNotNone(self.spi.start_requests())

    def test_synonym_requests(self):
        # A test for the synonym request function
        self.spi._sources = []

        src = Source()
        self.spi.add_source(src)
        self.assertEqual(self.spi.get_synonym_requests("new_compound"), [])
        self.assertIn("new_compound", self.spi.synonyms)

        src2 = ChemSpider()
        self.spi.add_source(src2)
        self.assertIsInstance(self.spi.get_synonym_requests("other_compound")[0], Request)
        self.assertIn("other_compound", self.spi.synonyms)
        self.assertEqual(self.spi.get_synonym_requests("other_compound"), [])