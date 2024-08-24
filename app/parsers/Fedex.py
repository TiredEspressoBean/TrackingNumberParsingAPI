import re
from functools import partial
from app.parsers.base_parser import BaseParser


class FedEx(BaseParser):
    def __init__(self):
        self.constructors = [
            "SerialNumber",
            "CheckDigit",
            "DestinationZip",
            "ShippingContainerType",
            "ApplicationIdentifier",
            "SCNC",
            "ServiceType",
            "ShipperId",
            "PackageId",
            "GSN",
        ]

        # Because FedEx mixes and matches its methods of validating tracking numbers we use partial functions with
        #   parameters already set in them.
        self.patterns = {
            "FedEx Express(12)": [
                r'(?P<SerialNumber>([0-9]\s*){11})(?P<CheckDigit>[0-9])',
                partial(self.sum_product_with_weightings_and_modulo,
                        weightings=[3, 1, 7, 3, 1, 7, 3, 1, 7, 3, 1],
                        modulo1=11,
                        modulo2=10)
            ],

            "FedEx Express(34)": [
                r'1\s*0\s*[0-9]\s*[0-9]\s*[0-9]\s*(?P<DestinationZip>[0-9]\s*){5}(?P<SerialNumber>[0-9]\s*){13}(?P<CheckDigit>[0-9])',
                partial(self.sum_product_with_weightings_and_modulo,
                        weightings=[1, 7, 3, 1, 7, 3, 1, 7, 3, 1, 7, 3, 1],
                        modulo1=11,
                        modulo2=10)
            ],
            "FedEx SmartPost": [
                r'(?:(?:(?P<RoutingApplicationId>4\s*2\s*0\s*)(?P<DestinationZip>[0-9]\s*){5})?(?P<ApplicationIdentifier>9\s*2\s*))?(?P<SerialNumber>(?P<SCNC>[0-9]\s*){2}(?P<ServiceType>2\s*9\s*)(?P<ShipperId>[0-9]\s*){8}(?P<PackageId>[0-9]\s*){11}|[0-9]\s*)?(?P<CheckDigit>[0-9]\s*)',
                partial(self.calculate_checksum_mod10, even_multiplier=3, odd_multiplier=1),
            ],
            "FedEx Ground": [
                r'(?P<SerialNumber>[0-9]\s*){14}(?P<CheckDigit>[0-9])',
                partial(self.calculate_checksum_mod10, even_multiplier=1, odd_multiplier=3),
            ],
            "FedEx Ground(SSCC-18)": [
                r'(?P<ShippingContainerType>[0-9]\s*){2}(?P<SerialNumber>[0-9]\s*){15}(?P<CheckDigit>[0-9])',
                partial(self.calculate_checksum_mod10, even_multiplier=3, odd_multiplier=1),
            ],
            "FedEx Ground96(22)": [
                r'(?P<ApplicationIdentifier>9\s*6\s*)(?P<SCNC>[0-9]\s*){2}(?P<ServiceType>[0-9]\s*){3}(?P<SerialNumber>(?P<ShipperId>[0-9]\s*){7}(?P<PackageId>[0-9]\s*){7})(?P<CheckDigit>[0-9])',
                partial(self.calculate_checksum_mod10, even_multiplier=1, odd_multiplier=3),
            ],
            "FedEx Ground GSN": [
                r'(?P<ApplicationIdentifier>9\s*6\s*)(?P<SCNC>[0-9]\s*){2}[0-9]\s*{5}(?P<GSN>[0-9]\s*){10}[0-9]\s*(?P<SerialNumber>[0-9]\s*){13}(?P<CheckDigit>[0-9])',
                partial(self.sum_product_with_weightings_and_modulo,
                        weightings=[3, 1, 7, 3, 1, 7, 3, 1, 7, 3, 1],
                        modulo1=11,
                        modulo2=10)
            ]
        }

        self.tracking_url = "https://www.fedex.com/apps/fedextrack/?tracknumbers=%s"

    def validate(self, tracking_number):
        """
        Validate a tracking number as being a FedEx tracking number or not.
        :param tracking_number: String of the tracking number to check.
        :return: Bool of whether the string is valid as a DHL tracking number or not.
        """
        for pattern_name, (regex, validation_func) in self.patterns.items():
            match = re.match(regex, tracking_number)
            if match:
                # Extract the fields required for validation
                check_digit = match.group("CheckDigit")
                serial_number = match.group("SerialNumber")

                # Call the validation function
                valid = validation_func(serial_number=serial_number, check_digit=check_digit)
                if valid:
                    return True

        return False

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
            "carrier": "FedEx",
            "trackingNumber": tracking_number,
            "serialNumber": "",
            "trackingUrl": self.tracking_url % tracking_number
        }
        for key, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.match(pattern, tracking_number)
                if match:
                    for constructor in self.constructors:
                        if constructor in match.groupdict():
                            ret[constructor] = match.group(constructor)
                    return ret
