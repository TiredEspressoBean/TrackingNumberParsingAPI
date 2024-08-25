import importlib
import pkgutil
from app.parsers.base_parser import BaseParser


class ParseManager:
    def __init__(self):
        self.parsers = []
        self.__load_parsers()

    def __load_parsers(self):
        """
        Set up the engine with all the current parsers currently available
        :return: None
        """
        for finder, name, ispkg in pkgutil.iter_modules(['app/parsers']):
            if name != 'base_parser' and name != 'BaseParser':
                module = importlib.import_module(f'app.parsers.{name}')
                for attr in dir(module):
                    parser_class = getattr(module, attr)
                    if isinstance(parser_class, type) and issubclass(parser_class, BaseParser) and attr != 'BaseParser':
                        parser_instance = parser_class()
                        self.parsers.append(parser_instance)

    def get_parsers(self, tracking_numbers):
        response = []
        for tracking_number in tracking_numbers:
            for parser in self.parsers:
                try:
                    data = parser.parse(tracking_number)
                except Exception as e:
                    continue
                if data:
                    response.append(data)
            return response