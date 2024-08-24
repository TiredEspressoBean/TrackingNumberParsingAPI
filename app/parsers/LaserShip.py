import re
from functools import partial
from app.parsers.base_parser import BaseParser


class LaserShip(BaseParser):
    def __init__(self):
        self.carrier_name = 'LaserShip'
        self.tracking_url_template = ''
        self.patterns = [
            r'\s*L\s*[AIEHNX]\s*[1-3]\s*(?P<SerialNumber>([0-9]\s*){7})\s*',
            r'\s*1\s*L\s*S\s*7\s*[12]\s*([0-9]\s*){4}(?P<SerialNumber>([0-9]\s*){6})\s*',
            r'\s*1\s*L\s*S\s*7\s*[12]\s*([0-9]\s*){2}\s*0\s*1\s*[1234]\s*(?P<SerialNumber>([0-9]\s*){6})-\s*1\s*'
        ]
        self.constructors = [
            "SerialNumber",
        ]

    def validate(self, tracking_number: str) -> bool:
        """
        Validate a tracking number as being a LaserShip tracking number or not.
        :param tracking_number: String of the tracking number to check.
        :return: Bool of whether the string is valid as a DHL tracking number or not.
        """
        for pattern in self.patterns:
            match = re.match(pattern, tracking_number)
            if match:
                return True
        return False

    def parse(self, tracking_number: str) -> dict or None:
        """
        Parse a tracking number of the information that is available from the tracking number
        :param tracking_number: String of the tracking number to parse.
        :return: Dictionary object with all information that could be parsed from the tracking number
        """
        if not self.validate(tracking_number):
            return
        ret = {
            "carrier": self.carrier_name,
            "trackingNumber": tracking_number,
            "trackingUrl": self.tracking_url_template % tracking_number
        }
        for pattern in self.patterns:
            match = re.search(pattern, tracking_number)
            if match:
                for constructor in self.constructors:
                    if match.groupdict().get(constructor):  # Check if constructor is in match groups
                        ret[constructor] = match.group(constructor)
                return ret