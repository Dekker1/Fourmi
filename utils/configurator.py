import ConfigParser

from scrapy.utils.project import get_project_settings


class Configurator:
    """
    A helper class in the fourmi class. This class is used to process the settings as set
    from one of the Fourmi applications.
    """

    def __init__(self):
        self.scrapy_settings = get_project_settings()


    def set_output(self, filename, fileformat):
        """
        This function manipulates the Scrapy output file settings that normally would be set in the settings file.
        In the Fourmi project these are command line arguments.
        :param filename: The filename of the file where the output will be put.
        :param fileformat: The format in which the output will be.
        """

        if filename != 'results.*format*':
            self.scrapy_settings.overrides["FEED_URI"] = filename
        elif fileformat == "jsonlines":
            self.scrapy_settings.overrides["FEED_URI"] = "results.json"
        elif fileformat is not None:
            self.scrapy_settings.overrides["FEED_URI"] = "results." + fileformat

        if fileformat is not None:
            self.scrapy_settings.overrides["FEED_FORMAT"] = fileformat


    def set_logging(self, logfile=None, verbose=0):
        """
        This function changes the default settings of Scapy's logging functionality
        using the settings given by the CLI.
        :param logfile: The location where the logfile will be saved.
        :param verbose: A integer value to switch between loglevels.
        """
        if verbose != 0:
            self.scrapy_settings.overrides["LOG_ENABLED"] = True
        else:
            self.scrapy_settings.overrides["LOG_ENABLED"] = False

        if verbose == 1:
            self.scrapy_settings.overrides["LOG_LEVEL"] = "WARNING"
        elif verbose == 2:
            self.scrapy_settings.overrides["LOG_LEVEL"] = "INFO"
        else:
            self.scrapy_settings.overrides["LOG_LEVEL"] = "DEBUG"

        if verbose > 1:
            self.scrapy_settings.overrides["LOG_STDOUT"] = False
        else:
            self.scrapy_settings.overrides["LOG_STDOUT"] = True

        if logfile is not None:
            self.scrapy_settings.overrides["LOG_FILE"] = logfile
        else:
            self.scrapy_settings.overrides["LOG_FILE"] = None


    @staticmethod
    def read_sourceconfiguration():
        """
        This function reads sources.cfg in the main folder for configuration
        variables for sources
        :return a ConfigParser object of sources.cfg
        """
        config = ConfigParser.ConfigParser()
        config.read('sources.cfg') # [TODO]: should be softcoded eventually
        return config

    @staticmethod
    def get_section(config, sourcename):
        """
        This function reads a config section labeled in variable sourcename and
        tests whether the reliability variable is set else set to empty string.
        Return the default section if the labeled config section does not exist
        :param config: a ConfigParser object
        :param sourcename: the name of the section to be read
        :return a dictionary of the section in the config labeled in sourcename
        """
        section = dict()
        if config.has_section(sourcename):
            section = dict(config.items(sourcename))
        elif config.defaults():
            section = config.defaults()
        if 'reliability' not in section:
            print 'WARNING: Reliability not set for %s' % sourcename
            section['reliability'] = ''
        return section
