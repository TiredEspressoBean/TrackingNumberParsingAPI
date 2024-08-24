import re


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


# Example usage
serial_number = "986578788855"
weightings = [3, 1, 7, 3, 1, 7, 3, 1, 7, 3, 1]
modulo1 = 11
modulo2 = 10

# Define regex pattern
pattern = r'\s*(?P<SerialNumber>([0-9]\s*){11})(?P<CheckDigit>[0-9]\s*)'

# Use regex to extract SerialNumber and CheckDigit
match = re.match(pattern, serial_number)
if match:
    serial_number = match.group("SerialNumber")
    check_digit = match.group("CheckDigit")

    # Validate checksum
    is_valid = sum_product_with_weightings_and_modulo(serial_number, check_digit, weightings, modulo1, modulo2)
    print(f"Checksum valid: {is_valid}")
else:
    print("Invalid format")