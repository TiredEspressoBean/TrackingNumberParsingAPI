import re
from app.parsers.base_parser import BaseParser


class AmazonParser(BaseParser):
    def __init__(self):
        self.constructors = [
            "serialNumber"
        ]
        self.patterns = [
            r'^T\s*B\s*A\s*(?P<serialNumber>[0-9]{12})$'
        ]
        self.tracking_url = "https://track.amazon.com/tracking/0?trackingId="

    def validate(self, tracking_number: str) -> bool:
        """
        Validation for Amazon tracking number.
        :param tracking_number: String of Amazon tracking number.
        :return: Bool of whether the tracking number is valid for Amazon tracking.
        """
        for pattern in self.patterns:
            match = re.match(pattern, tracking_number)
            if match:
                return True
        return False

    def parse(self, tracking_number: str) -> dict or None:
        """
        Parse Amazon tracking number, and return as dictionary object with all information.
        :param tracking_number: String of Amazon tracking number.
        :return: Dictionary object of information as parsed from the Amazon tracking number.
        """
        if not self.validate(tracking_number):
            return
        ret = {
            "carrier": "Amazon",
            "trackingNumber": tracking_number,
            "serialNumber": "",
            "trackingUrl": self.tracking_url + str(tracking_number)
        }
        for pattern in self.patterns:
            for constructor in self.constructors:
                match = re.search(pattern, tracking_number)
                if match:
                    ret[constructor] = match.group(constructor)
        return ret
