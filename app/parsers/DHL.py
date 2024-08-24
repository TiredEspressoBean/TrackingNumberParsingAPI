import re
from app.parsers.base_parser import BaseParser


class DHL(BaseParser):
    def __init__(self):
        self.constructors = [
            "SerialNumber",
            "CheckDigit",
        ]
        self.patterns = [
            r'(?P<SerialNumber>\d{9,10})(?P<CheckDigit>\d)',
            r'((GM)|(LX)|(RX)|(UV)|(CN)|(SG)|(TH)|(IN)|(HK)|(MY))\s*(?P<SerialNumber>\d{10,39})'
        ]
        self.carrier_name = "DHL"
        self.tracking_url = "http://www.dhl.com/en/express/tracking.html?brand=DHL&AWB=%s"

    def validate(self, tracking_number):
        """
        Validate a tracking number as being a DHL tracking number or not.
        :param tracking_number: String of the tracking number to check.
        :return: Bool of whether the string is valid as a DHL tracking number or not.
        """
        for pattern in self.patterns:
            match = re.match(pattern, tracking_number)
            if not match:
                continue
            if match and match.group("CheckDigit"):
                check_digit = int(match.group("CheckDigit"))
                serial_number = match.group("SerialNumber")
                mod_test = self.calculate_checksum_mod7([int(x) for x in serial_number], check_digit, 1, 1)
                return mod_test
            return True

    def parse(self, tracking_number):
        """
        Parse a tracking number of the information that is available from the tracking number
        :param tracking_number: String of the tracking number to parse.
        :return: Dictionary object with all information that could be parsed from the tracking number
        """
        valid = self.validate(tracking_number)
        if not valid:
            return
        ret = {
            "carrier": self.carrier_name,
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
