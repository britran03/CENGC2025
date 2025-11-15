import string
import base64

# Define character sets for conversions
NUMBER_CHARS = string.digits + string.ascii_uppercase
BASE64_CHARS = string.ascii_uppercase + string.ascii_lowercase + string.digits + "+/"


def to_base_10(number: str, from_base: int) -> int:
    """Converts a string in a given base (2-36) to a base 10 integer."""
    if not (2 <= from_base <= len(NUMBER_CHARS)) and from_base != 64:
        raise ValueError(f"Base must be between 2 and {len(NUMBER_CHARS)}")

    chars = NUMBER_CHARS
    if from_base == 64:
        chars = BASE64_CHARS
    number = number.upper()
    total = 0
    for i, char in enumerate(reversed(number)):
        # Just ignore and keep going if the character isn't valid
        if char in chars:
            value = chars.index(char)
            total += value * (from_base**i)
    return total


def from_base_10(number: int, to_base: int) -> str:
    """Converts a base 10 integer to a string in a specified base (2-36)."""
    chars = NUMBER_CHARS
    if to_base == 64:
        chars = BASE64_CHARS

    if number == 0:
        return "0"
    encoded_string = ""
    while number > 0:
        encoded_string = chars[number % to_base] + encoded_string
        number //= to_base
    return encoded_string


def convert_number_base(number: str, from_base: int, to_base: int) -> str | None:
    """Converts from one numerical base to another."""
    try:
        base_10_val = to_base_10(number, from_base)
        return from_base_10(base_10_val, to_base)
    except ValueError:
        return None


def convert_number_to_string(number: str, from_base: int) -> str | None:
    """Converts a space-separated string of numbers into an ascii string."""
    try:
        char_codes = [to_base_10(num, from_base) for num in number.split()]
        return "".join(chr(code) for code in char_codes)
    except ValueError:
        return None


def convert_string_to_number(string: str, to_base: int) -> str | None:
    """Converts an ascii string into a space-separated string of numbers."""
    try:
        char_codes = [ord(char) for char in string]
        return " ".join(from_base_10(code, to_base) for code in char_codes)
    except ValueError:
        return None


def convert_string_to_base64(string: str) -> str | None:
    """Converts an ascii string to base64"""
    return base64.b64decode(string).decode("utf-8")


def convert_base64_to_string(b64_string: str) -> str | None:
    """Decodes a Base64 string to a UTF-8 string using the standard library."""
    try:
        return base64.b64decode(b64_string).decode("utf-8")
    except ValueError:
        return None


def convert_base64_to_number(b64_string: str, to_base: int) -> str | None:
    """
    Converts a Base64 string to a numerical representation in the specified base
    using arithmetic conversion.
    """
    try:
        decoded_bytes = base64.b64decode(b64_string)
        number = int.from_bytes(decoded_bytes, "big")
        return from_base_10(number, to_base)
    except ValueError:
        return None


def convert_number_to_base64(number_str: str, from_base: int) -> str | None:
    """
    Converts a number string in a specified base to its Base64 representation
    using arithmetic conversion.
    """
    try:
        number = to_base_10(number_str, from_base)
        # Determine the number of bytes needed and convert
        num_bytes = (number.bit_length() + 7) // 8
        if num_bytes == 0:  # Handle the case where the number is 0
            num_bytes = 1
        byte_representation = number.to_bytes(num_bytes, "big")
        return base64.b64encode(byte_representation).decode("ascii")
    except ValueError:
        return None
