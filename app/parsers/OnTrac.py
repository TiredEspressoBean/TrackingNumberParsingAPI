import re
from functools import partial
from app.parsers.base_parser import BaseParser


class OnTrac(BaseParser):
    def __init__(self):
        self.carrier_name = "OnTrac"
        self.tracking_url_template = "http://www.ontrac.com/tracking/?number=%s"
        self.constructors = [
            "SerialNumber",
            "CheckDigit"
        ]
        self.patterns = [
            r'\s*C\s*(?P<SerialNumber>([0-9]\s*){13})(?P<CheckDigit>[0-9])',
            r'\s*D\s*(?P<SerialNumber>([0-9]\s*){13})(?P<CheckDigit>[0-9])'

        ]

    def validate(self, tracking_number: str) -> bool:
        """
        Validate a tracking number as being an OnTrac tracking number or not.
        :param tracking_number: String of the tracking number to check.
        :return: Bool of whether the string is valid as a DHL tracking number or not.
        """
        for pattern in self.patterns:
            if not re.search(pattern, tracking_number):
                continue
            match = re.match(pattern, tracking_number)
            check_digit = int(match.group('CheckDigit'))
            serial_number = [int(x) for x in match.group('SerialNumber')]

            # OnTrac does something similar to UPS where part of the serial number to be parsed is either 4, or 5
            #   depending on whether it starts with C or D respectively.
            if tracking_number[0] == "C":
                serial_number.insert(0, 4)
            elif tracking_number[0] == "D":
                serial_number.insert(0, 5)
            valid = self.calculate_checksum_mod10(serial_number, check_digit, 1, 2)
            return valid

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