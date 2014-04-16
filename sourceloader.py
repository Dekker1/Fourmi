import inspect
import os
from FourmiCrawler.parsers.parser import Parser


class SourceLoader:
    sources = []

    def __init__(self, rel_dir="FourmiCrawler/parsers"):
        path = os.path.dirname(os.path.abspath(__file__))
        path += "/" + rel_dir
        known_parser = set()

        for py in [f[:-3] for f in os.listdir(path) if f.endswith('.py') and f != '__init__.py']:
            mod = __import__('.'.join([rel_dir.replace("/", "."), py]), fromlist=[py])
            classes = [getattr(mod, x) for x in dir(mod) if inspect.isclass(getattr(mod, x))]
            for cls in classes:
                if issubclass(cls, Parser) and cls not in known_parser:
                    self.sources.append(cls())  # [review] - Would we ever need arguments for the parsers?
                    known_parser.add(cls)

    def include(self, source_names):
        pass # [todo] - implement source inclusion.

    def exclude(self, source_names):
        pass # [todo] - implement source exclusion.

    def __str__(self):
        string = ""
        for src in self.sources:
            string += "Source: " + src.__class__.__name__
            string += " - "
            string +=  "URI: " + src.website + "\n"
        return string