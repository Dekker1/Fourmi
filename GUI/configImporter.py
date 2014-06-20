import ConfigParser


class ConfigImporter():
    def __init__(self, filename):
        """Read the filename into the parser."""
        self.filename = filename
        self.parser = ConfigParser.ConfigParser()
        self.parser.read(self.filename)

    def load_common_attributes(self):
        """Loads common attributes from the initialized file."""
        try:
            return self.parser.get('GUI', 'CommonParameters')
        except:
            return 'One, Two, Three'

    def load_output_types(self):
        """Loads output types from the initialized file."""
        try:
            return self.parser.get('GUI', 'OutputTypes')
        except:
            return 'csv'

    def load_always_attributes(self):
        """Loads attributes that are always searched for from the initialized file."""
        try:
            return self.parser.get('GUI', 'AlwaysParameters')
        except:
            return 'Name, Weight'
