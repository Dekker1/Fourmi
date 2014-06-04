import unittest

from sourceloader import SourceLoader


class TestSourceloader(unittest.TestCase):

    def setUp(self):
        self.loader = SourceLoader()

    def test_init(self):
        # Test if sourceloader points to the right directory, where the sources are present.
        self.assertIn("Source: Source", str(self.loader))
        self.assertIn("Source: NIST", str(self.loader))
        self.assertIn("Source: ChemSpider", str(self.loader))
        self.assertIn("Source: WikipediaParser", str(self.loader))

    def test_include(self):
        #Tests for the include functionality.
        self.loader.include(["So.rc.*"])

        self.assertIn("Source: Source", str(self.loader))
        self.assertNotIn("Source: NIST", str(self.loader))
        self.assertNotIn("Source: ChemSpider", str(self.loader))
        self.assertNotIn("Source: WikipediaParser", str(self.loader))

    def test_exclude(self):
        #Tests for the exclude functionality.
        self.loader.exclude(["So.rc.*"])

        self.assertNotIn("Source: Source", str(self.loader))
        self.assertIn("Source: NIST", str(self.loader))
        self.assertIn("Source: ChemSpider", str(self.loader))
        self.assertIn("Source: WikipediaParser", str(self.loader))
