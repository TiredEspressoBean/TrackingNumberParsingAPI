import re
from app.parsers.base_parser import BaseParser

class USPSParser(BaseParser):
    def __init__(self):
        self.carrier_name = "United States Postal Service"
        self.tracking_url_template = "https://tools.usps.com/go/TrackConfirmAction?tLabels=%s"

        self.constructors = [
            "ServiceType", "ShipperId", "PackageId", "CheckDigit",
            "DestinationZip", "RoutingNumber", "ApplicationIdentifier", "SCNC"
        ]

        self.patterns = [
            # USPS 20 format
            r"\s*(?P<ServiceType>([0-9]\s*){2})(?P<ShipperId>([0-9]\s*){9})(?P<PackageId>([0-9]\s*){8})(?P<CheckDigit>[0-9]\s*)",
            # USPS 34v2 format
            r"\s*420\s*(?P<DestinationZip>([0-9]\s*){5})(?P<RoutingNumber>([0-9]\s*){4})(?P<ShipperId>([0-9]\s*){8})(?P<PackageId>([0-9]\s*){11})(?P<CheckDigit>[0-9]\s*)",
            # USPS 91 format
            r"\s*(420\s*(?P<DestinationZip>([0-9]\s*){5}))?\s*(?P<ApplicationIdentifier>9\s*[12345]\s*)?(?P<SCNC>([0-9]\s*){2})(?P<ServiceType>([0-9]\s*){2})(?P<ShipperId>([0-9]\s*){8})(?P<PackageId>([0-9]\s*){11}|([0-9]\s*){7})(?P<CheckDigit>[0-9]\s*)"
        ]

    def validate(self, tracking_number: str) -> bool:
        """
        Validate a tracking number as being a UPS tracking number or not.
        :param tracking_number: String of the tracking number to check.
        :return: Bool of whether the string is valid as a DHL tracking number or not.
        """
        for pattern in self.patterns:
            if not re.search(pattern, tracking_number):
                continue
            match = re.match(pattern, tracking_number)
            check_digit = int(match.group("CheckDigit"))
            package_id = tracking_number[:-1]
            if self.calculate_checksum_mod10([int(x) for x in package_id], check_digit, 3, 1):
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
                    if match.groupdict().get(constructor):
                        ret[constructor] = match.group(constructor)
        return ret
