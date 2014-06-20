import unittest
import ConfigParser

from utils.configurator import Configurator


class TestConfigurator(unittest.TestCase):

    def setUp(self):
        self.conf = Configurator()

    def test_set_output(self):
        self.conf.set_output(filename="test.txt", fileformat="csv", compound="test")
        self.assertEqual(self.conf.scrapy_settings["FEED_URI"], "test.txt")
        self.assertEqual(self.conf.scrapy_settings["FEED_FORMAT"], "csv")

        self.conf.set_output("<compound>.*format*", "jsonlines", "test")
        self.assertEqual(self.conf.scrapy_settings["FEED_URI"], "test.json")
        self.assertEqual(self.conf.scrapy_settings["FEED_FORMAT"], "jsonlines")

        self.conf.set_output("<compound>.*format*", "csv", "test")
        self.assertEqual(self.conf.scrapy_settings["FEED_URI"], "test.csv")
        self.assertEqual(self.conf.scrapy_settings["FEED_FORMAT"], "csv")

    def test_start_log(self):
        for i in range(0, 3):
            self.conf.set_logging("TEST", i)
            self.assertEqual(self.conf.scrapy_settings.get("LOG_FILE"), "TEST")
            if i > 0:
                self.assertEqual(self.conf.scrapy_settings.get("LOG_ENABLED"), True)
                if i > 1:
                    self.assertEqual(self.conf.scrapy_settings.get("LOG_STDOUT"), False)
                else:
                    self.assertEqual(self.conf.scrapy_settings.get("LOG_STDOUT"), True)
            else:
                self.assertEqual(self.conf.scrapy_settings.get("LOG_ENABLED"), False)
                self.assertEqual(self.conf.scrapy_settings.get("LOG_STDOUT"), True)
            if i == 1:
                self.assertEqual(self.conf.scrapy_settings.get("LOG_LEVEL"), "WARNING")
            elif i == 2:
                self.assertEqual(self.conf.scrapy_settings.get("LOG_LEVEL"), "INFO")
            elif i == 3:
                self.assertEqual(self.conf.scrapy_settings.get("LOG_LEVEL"), "DEBUG")

            self.conf.set_logging(verbose=i)
            self.assertEqual(self.conf.scrapy_settings.get("LOG_FILE"), None)

    def test_read_sourceconfiguration(self):
        config = self.conf.read_sourceconfiguration()
        self.assertIsInstance(config, ConfigParser.ConfigParser)

    def test_get_section(self):
        config = ConfigParser.ConfigParser()
        section = self.conf.get_section(config, 'test')
        self.assertIn('reliability', section)
        self.assertEquals(section['reliability'], '')

        config.set('DEFAULT', 'reliability', 'Low')

        section = self.conf.get_section(config, 'test')
        self.assertEquals(section['reliability'], 'Low')

        config.add_section('test')
        config.set('test', 'var', 'Maybe')

        section = self.conf.get_section(config, 'test')
        self.assertEquals(section['reliability'], 'Low')
        self.assertEqual(section['var'], 'Maybe')
