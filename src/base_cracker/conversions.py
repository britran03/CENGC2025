import string
import base64

# Define character sets for conversions
NUMBER_CHARS = string.digits + string.ascii_uppercase
BASE64_CHARS = string.ascii_uppercase + string.ascii_lowercase + string.digits + "+/"


def to_base_10(number: str, from_base: int) -> int:
    """Converts a string in a given base (2-36) or base 64 to a base 10 integer."""
    chars = NUMBER_CHARS
    base_max = len(NUMBER_CHARS)
    if from_base == 64:
        chars = BASE64_CHARS
        base_max = 64

    if not (2 <= from_base <= base_max):
        raise ValueError(f"Base must be between 2 and {base_max}")

    total = 0
    for i, char in enumerate(reversed(number)):
        # Skip invalid characters to be more forgiving
        if char in chars:
            value = chars.index(char)
            if value >= from_base:
                continue  # Skip digits that are out of range for the base
            total += value * (from_base**i)
    return total


def from_base_10(number: int, to_base: int) -> str:
    """Converts a base 10 integer to a string in a specified base (2-36 or 64)."""
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


def convert_number_base(number: str, from_base: int, to_base: int) -> str | None:
    """Converts from one numerical base to another."""
    try:
        base_10_val = to_base_10(number, from_base)
        return from_base_10(base_10_val, to_base)
    except Exception:
        return None


def convert_number_to_string(numbers_str: str, from_base: int) -> str | None:
    """Converts a space-separated string of numbers into an ASCII string."""
    try:
        char_codes = [to_base_10(num, from_base) for num in numbers_str.split()]
        return "".join(chr(code) for code in char_codes)
    except Exception:
        return None


def convert_string_to_number(text: str, to_base: int) -> str | None:
    """Converts an ASCII string into a space-separated string of numbers."""
    try:
        char_codes = [ord(char) for char in text]
        return " ".join(from_base_10(code, to_base) for code in char_codes)
    except (ValueError, TypeError):
        return None


def convert_string_to_base64(text: str) -> str | None:
    """Encodes a string to Base64."""
    try:
        return base64.b64encode(text.encode("utf-8")).decode("ascii")
    except Exception:
        return None


def convert_base64_to_string(b64_string: str) -> str | None:
    """Decodes a Base64 string to a UTF-8 string."""
    try:
        # Add padding if it's missing
        missing_padding = len(b64_string) % 4
        if missing_padding:
            b64_string += "=" * (4 - missing_padding)
        return base64.b64decode(b64_string).decode("utf-8")
    except Exception:
        return None
