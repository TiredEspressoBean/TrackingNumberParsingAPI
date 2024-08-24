import re
from app.parsers.base_parser import BaseParser

class UPSParser(BaseParser):
    def __init__(self):
        self.carrier_name = "UPS"
        self.tracking_url_template = "https://wwwapps.ups.com/WebTracking/track?track=yes&trackNums=%s"

        self.constructors = [
            "SerialNumber", "ShipperId", "ServiceTypeCode", "PackageId", "CheckDigit",
            "ServiceTypeLookup"
        ]

        self.patterns = [
            # UPS standard tracking number format
            r"^\s*1\s*Z\s*(?P<ShipperId>([A-Z0-9]\s*){6})(?P<ServiceTypeCode>([A-Z0-9]\s*){2})(?P<PackageId>([A-Z0-9]\s*){7})(?P<CheckDigit>[0-9]\s*)$",
            # UPS Waybill tracking number format
            r"\s*(?P<ServiceTypeCode>[AHJKTV]\s*)(?P<SerialNumber>([0-9]\s*){9})(?P<CheckDigit>[0-9]\s*)$"
        ]

        # Define service type lookups
        self.service_type_lookup = {
            "01": "UPS United States Next Day Air (Red)",
            "02": "UPS United States Second Day Air (Blue)",
            "03": "UPS United States Ground",
            "12": "UPS United States Third Day Select",
            "13": "UPS United States Next Day Air Saver (Red Saver)",
            "15": "UPS United States Next Day Air Early A.M.",
            "22": "UPS United States Ground - Returns Plus - Three Pickup Attempts",
            "32": "UPS United States Next Day Air Early A.M. - COD",
            "33": "UPS United States Next Day Air Early A.M. - Saturday Delivery, COD",
            "41": "UPS United States Next Day Air Early A.M. - Saturday Delivery",
            "42": "UPS United States Ground - Signature Required",
            "44": "UPS United States Next Day Air - Saturday Delivery",
            "66": "UPS United States Worldwide Express",
            "72": "UPS United States Ground - Collect on Delivery",
            "78": "UPS United States Ground - Returns Plus - One Pickup Attempt",
            "90": "UPS United States Ground - Returns - UPS Prints and Mails Label",
            "A0": "UPS United States Next Day Air Early A.M. - Adult Signature Required",
            "A1": "UPS United States Next Day Air Early A.M. - Saturday Delivery, Adult Signature Required",
            "A2": "UPS United States Next Day Air - Adult Signature Required",
            "A8": "UPS United States Ground - Adult Signature Required",
            "A9": "UPS United States Next Day Air Early A.M. - Adult Signature Required, COD",
            "AA": "UPS United States Next Day Air Early A.M. - Saturday Delivery, Adult Signature Required, COD",
            "YW": "UPS SurePost - Delivered by the USPS",
            "J": "UPS Next Day Express",
            "K": "UPS Ground",
            "V": "UPS WorldWide Express Saver"
        }

    def validate(self, tracking_number: str) -> bool:
        """
        Validate a tracking number as being a UPS tracking number or not.
        :param tracking_number: String of the tracking number to check.
        :return: Bool of whether the string is valid as a DHL tracking number or not.
        """
        for pattern in self.patterns:
            # Check digit operations may have been discontinued for UPS?
            # match = re.match(pattern, tracking_number)
            # if match.groupdict().get("CheckDigit") == sum(match.groupdict()["CheckDigit"]):
            if re.search(pattern, tracking_number):
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

                # Check if the service type is in the lookup and if so add that to the return since we can
                service_type_code = ret["ServiceTypeCode"].replace(" ", "")
                if service_type_code in self.service_type_lookup:
                    ret["ServiceType"] = self.service_type_lookup[service_type_code]
                return ret
