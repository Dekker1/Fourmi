from scrapy import log
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


    def start_log(self, logfile, verbose):
        """
        This function starts the logging functionality of Scrapy using the settings given by the CLI.
        :param logfile: The location where the logfile will be saved.
        :param verbose: A boolean value to switch between loglevels.
        """
        if logfile is not None:
            if verbose:
                log.start(logfile=logfile, logstdout=False, loglevel=log.DEBUG)
            else:
                log.start(logfile=logfile, logstdout=True, loglevel=log.WARNING)
        else:
            if verbose:
                log.start(logstdout=False, loglevel=log.DEBUG)
            else:
                log.start(logstdout=True, loglevel=log.WARNING)
