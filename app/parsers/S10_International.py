import re
from app.parsers.base_parser import BaseParser


class s10International(BaseParser):
    def __init__(self):
        self.constructors = [
            "ServiceTypeCode",
            "SerialNumber",
            "CheckDigit",
            "CountryCode"
        ]
        self.patterns = [
            r'(?P<ServiceTypeCode>[A-Z]{2})\s*(?P<SerialNumber>[0-9]{8})\s*(?P<CheckDigit>[0-9])\s*(?P<CountryCode>[A-Z]{2})'
        ]
        self.service_type_lookup = {
            "E[A-Z]": "EMS",
            "L[A-Z]": "Letter Post Express",
            "M[A-Z]": "Letter Post M-bag",
            "Q[A-M]": "Letter Post IBRS",
            "R[A-Z]": "Letter Post Registered",
            "U[A-Z]": "Letter Post Misc",
            "V[A-Z]": "Letter Post Insured",
            "C[A-Z]": "Parcel Post",
            "H[A-Z]": "Parcel Post (e-commerce)",
            "([BDNPZ][A-Z]|A[V-Z]|G[AD])": "Domestic"
        }

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
            check_digit = int(match.group("CheckDigit"))
            serial_number = int(match.group("SerialNumber"))
            return self.s10_checksum(serial_number, check_digit)

    def parse(self, tracking_number: str) -> dict or None:
        """
        Parse a tracking number of the information that is available from the tracking number
        :param tracking_number: String of the tracking number to parse.
        :return: Dictionary object with all information that could be parsed from the tracking number
        """
        valid = self.validate(tracking_number)
        if not valid:
            return
        ret = {
            "carrier": "International",
            "trackingNumber": tracking_number,
        }
        for pattern in self.patterns:
            match = re.search(pattern, tracking_number)
            if match:
                for constructor in self.constructors:
                    if match.groupdict().get(constructor):
                        ret[constructor] = match.group(constructor)
            if "ServiceTypeCode" in ret:
                for service_type in self.service_type_lookup:
                    match = re.search(service_type, ret["ServiceTypeCode"])
                    if match:
                        ret["ServiceType"] = self.service_type_lookup[service_type]
                        break
        return ret

    @staticmethod
    def s10_checksum(serial_number, check_digit) -> bool:
        """
        Checksum algorithm specifically made for the S10 standard, using the version from the wikipedia article linked
        below.
        https://en.wikipedia.org/wiki/S10_(UPU_standard)
        :param serial_number: Int serial number to be parsed from
        :param check_digit: Digit for the sum of the parsed serial number to check against
        :return: Bool of whether the checksum is valid or not
        """
        # Checksum algo from wikipedia https://en.wikipedia.org/wiki/S10_(UPU_standard)
        weights = [8, 6, 4, 2, 3, 5, 9, 7]
        check_digit_sum = 0
        for i, digit in enumerate(f"{serial_number:08}"):
            check_digit_sum += weights[i] * int(digit)
        check_digit_sum = 11 - (check_digit_sum % 11)
        if check_digit_sum == 10:
            check_digit_sum = 0
        elif check_digit_sum == 11:
            check_digit_sum = 5
        return check_digit_sum == check_digit
