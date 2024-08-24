from abc import ABC, abstractmethod

class BaseParser(ABC):
    @abstractmethod
    def parse(self, tracking_number: str) -> dict:
        pass

    @abstractmethod
    def validate(self, tracking_number: str) -> bool:
        pass

    @staticmethod
    def normalize(self, tracking_number: str) -> str:
        return tracking_number.replace(' ', '').upper()

    @staticmethod
    def calculate_checksum_mod10(digits: list, check_digit: int, evens_multiplier: int, odds_multiplier: int) -> bool:
        """
        Static method to calculate and validate a checksum using Modulo 10 algorithm.

        :param digits: List of digits to process.
        :param check_digit: The expected check digit.
        :param evens_multiplier: Multiplier for digits in even positions.
        :param odds_multiplier: Multiplier for digits in odd positions.
        :return: True if the calculated check digit matches the expected check digit, False otherwise.
        """
        total = 0
        for i, digit in enumerate(digits):
            if i % 2 == 0:
                total += evens_multiplier * digit
            else:
                total += odds_multiplier * digit

        calculated_check_digit = (10 - (total % 10)) % 10
        return calculated_check_digit == check_digit

    @staticmethod
    def calculate_checksum_mod7(tracking_number: list, check_digit: int, even_multiplier, odd_multiplier) -> bool:
        """

        :param tracking_number: List of ints to process as review the checksum
        :param check_digit: Digit to check against the derived checksum
        :param even_multiplier: Multiplier for digits in even positions.
        :param odd_multiplier: Multiplier for digits in odd positions.
        :return: True if the calculated check digit matches the expected check digit, False otherwise.
        """
        total = 0
        for i, digit in enumerate(tracking_number):
            if i % 2 == 0:
                total += even_multiplier * digit
            else:
                total += odd_multiplier * digit
        calculated_check_digit = total % 7
        return calculated_check_digit == check_digit

    @staticmethod
    def sum_product_with_weightings_and_modulo(serial_number: str, check_digit: str, weightings: list, modulo1: int,
                                               modulo2: int) -> bool:
        """
        Validate a tracking number based on a checksum algorithm using weightings and modulo operations.

        :param serial_number: The serial number portion of the tracking number.
        :param check_digit: The check digit to validate against.
        :param weightings: List of weightings for the checksum calculation.
        :param modulo1: First modulo value for checksum validation.
        :param modulo2: Second modulo value for checksum validation.
        :return: True if the checksum is valid, otherwise False.
        """
        if len(serial_number) != len(weightings):
            raise ValueError("Serial number length does not match the length of weightings list.")
        digits = [int(digit) for digit in serial_number]
        weighted_sum = sum(digit * weight for digit, weight in zip(digits, weightings))
        checksum = weighted_sum % modulo1 % modulo2
        return int(check_digit) == checksum
