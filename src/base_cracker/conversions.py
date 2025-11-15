import string
import base64

# Define character sets for conversions
NUMBER_CHARS = string.digits + string.ascii_uppercase
BASE64_CHARS = string.ascii_uppercase + string.ascii_lowercase + string.digits + "+/"


def to_base_10(number_str: str, from_base: int) -> int:
    """Converts a string in a given base (3-36) or base 64 to a base 10 integer."""
    chars = NUMBER_CHARS
    base_max = len(NUMBER_CHARS)
    if from_base == 64:
        chars = BASE64_CHARS
        base_max = 64

    if not (2 <= from_base <= base_max):
        raise ValueError(f"Base must be between 2 and {base_max}")

    total = 0
    for i, char in enumerate(reversed(number_str)):
        # Skip invalid characters to be more forgiving
        if char in chars:
            value = chars.index(char)
            if value >= from_base:
                continue  # Skip digits that are out of range for the base
            total += value * (from_base**i)
    return total


def from_base_10(number: int, to_base: int) -> str:
    """Converts a base 10 integer to a string to a specified base (2-36 or 64)."""
    chars = NUMBER_CHARS
    if to_base == 64:
        chars = BASE64_CHARS

    if number == 0:
        return chars[0]

    encoded_string = ""
    while number > 0:
        encoded_string = chars[number % to_base] + encoded_string
        number //= to_base
    return encoded_string


def convert_number_base(number_str: str, from_base: int, to_base: int) -> str | None:
    """Converts from one numerical base to another."""
    try:
        base_10_val = to_base_10(number_str, from_base)
        return from_base_10(base_10_val, to_base)
    except Exception:
        return None


def convert_number_to_string(numbers_str: str, from_base: int) -> str | None:
    """Converts a number into an ascii string."""
    try:
        base = 256
        number = to_base_10(numbers_str, from_base)
        encoded_string = ""
        while number > 0:
            encoded_string = chr(number % base) + encoded_string
            number //= base
        return encoded_string
    except Exception:
        return None


def convert_string_to_number(text: str, to_base: int) -> str | None:
    """Converts an ascii string into a number of the specified base"""
    try:
        char_codes = [ord(char) for char in text]
        return "".join(from_base_10(code, to_base) for code in char_codes)
    except ValueError:
        return None


def convert_string_to_base64(text: str) -> str | None:
    """Convert an ascii string to base64."""
    try:
        return base64.b64encode(text.encode("ascii")).decode("ascii")
    except Exception:
        return None


def convert_base64_to_string(number_str: str) -> str | None:
    """Convert a base64 string to an ascii string."""
    try:
        # Add padding if it's missing
        missing_padding = len(number_str) % 4
        if missing_padding:
            number_str += "=" * (4 - missing_padding)
        return base64.b64decode(number_str).decode("ascii")
    except Exception:
        return None


def convert_number_to_base64(number_str: str, from_base: int) -> str | None:
    """Convert a number of the specified base to base64"""
    try:
        # Determine the number of bytes needed and convert the integer to bytes
        number = to_base_10(number_str, from_base)
        num_bytes = (number.bit_length() + 7) // 8
        byte_array = number.to_bytes(num_bytes, "big")
        # Encode the bytes using the standard Base64 library
        return base64.b64encode(byte_array).decode("ascii")
    except Exception:
        return None


def convert_base64_to_number(number_str: str, to_base: int) -> str | None:
    """Convert a base64 number into a number of the specified base"""
    try:
        decoded_bytes = base64.b64decode(number_str)
        return from_base_10(int.from_bytes(decoded_bytes, "big"), to_base)
    except Exception:
        return None
