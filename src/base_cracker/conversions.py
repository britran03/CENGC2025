import string
import base64

NUMBER_CHARS = string.digits + string.ascii_uppercase
BASE64_CHARS = string.ascii_uppercase + string.ascii_lowercase + string.digits + "+/"


def to_base_10(number_str: str, from_base: int) -> int:
    """Converts a string in a given base (2-36) to a base 10 integer.
    
    Note: This does NOT support base64 - use convert_base64_to_number for that.
    """
    if not (2 <= from_base <= 36):
        raise ValueError(f"Base must be between 2 and 36")

    total = 0
    for i, char in enumerate(reversed(number_str.upper())):
        if char in NUMBER_CHARS:
            value = NUMBER_CHARS.index(char)
            if value >= from_base:
                raise ValueError(f"Invalid digit '{char}' for base {from_base}")
            total += value * (from_base ** i)
    return total


def from_base_10(number: int, to_base: int) -> str:
    """Converts a base 10 integer to a string in the specified base (2-36).
    
    Note: This does NOT support base64 - use convert_number_to_base64 for that.
    """
    if not (2 <= to_base <= 36):
        raise ValueError(f"Base must be between 2 and 36")
    
    if number == 0:
        return "0"
    
    if number < 0:
        raise ValueError("Negative numbers are not supported")

    encoded_string = ""
    while number > 0:
        encoded_string = NUMBER_CHARS[number % to_base] + encoded_string
        number //= to_base
    return encoded_string


def convert_number_base(number_str: str, from_base: int, to_base: int) -> str | None:
    """Converts a number from one base (2-36) to another base (2-36).
    
    For base64 conversions, use the specialized base64 functions instead.
    """
    try:
        if from_base == 64 and to_base == 64:
            return number_str
        elif from_base == 64:
            return convert_base64_to_number(number_str, to_base)
        elif to_base == 64:
            return convert_number_to_base64(number_str, from_base)
        
        base_10_val = to_base_10(number_str, from_base)
        return from_base_10(base_10_val, to_base)
    except Exception:
        return None


def convert_number_to_string(numbers_str: str, from_base: int) -> str | None:
    """Converts a number (base 2-36) into an ASCII string.
    
    The number is treated as representing bytes, where each byte becomes a character.
    """
    try:
        number = to_base_10(numbers_str, from_base)
        
        if number == 0:
            return "\x00"
        
        encoded_string = ""
        while number > 0:
            encoded_string = chr(number % 256) + encoded_string
            number //= 256
        return encoded_string
    except Exception:
        return None


def convert_string_to_number(text: str, to_base: int) -> str | None:
    """Converts an ASCII string into a number of the specified base (2-36).
    
    Each character's ASCII value is converted separately and concatenated.
    """
    try:
        if not (2 <= to_base <= 36):
            raise ValueError(f"Base must be between 2 and 36")
        
        char_codes = [ord(char) for char in text]
        return "".join(from_base_10(code, to_base) for code in char_codes)
    except Exception:
        return None


def convert_string_to_base64(text: str) -> str | None:
    """Convert an ASCII string to base64."""
    try:
        return base64.b64encode(text.encode("utf-8")).decode("ascii")
    except Exception:
        return None


def convert_base64_to_string(base64_str: str) -> str | None:
    """Convert a base64 string to an ASCII string."""
    try:
        missing_padding = len(base64_str) % 4
        if missing_padding:
            base64_str += "=" * (4 - missing_padding)
        return base64.b64decode(base64_str).decode("utf-8")
    except Exception:
        return None


def convert_number_to_base64(number_str: str, from_base: int) -> str | None:
    """Convert a number (base 2-36) to base64.
    
    The number is converted to bytes, then base64 encoded.
    """
    try:
        if not (2 <= from_base <= 36):
            raise ValueError(f"Base must be between 2 and 36")
        
        number = to_base_10(number_str, from_base)
        
        if number == 0:
            return base64.b64encode(b'\x00').decode("ascii")
        
        num_bytes = (number.bit_length() + 7) // 8
        byte_array = number.to_bytes(num_bytes, "big")
        
        return base64.b64encode(byte_array).decode("ascii")
    except Exception:
        return None


def convert_base64_to_number(base64_str: str, to_base: int) -> str | None:
    """Convert a base64 string to a number in the specified base (2-36).
    
    The base64 is decoded to bytes, then converted to a number.
    """
    try:
        if not (2 <= to_base <= 36):
            raise ValueError(f"Base must be between 2 and 36")
        
        missing_padding = len(base64_str) % 4
        if missing_padding:
            base64_str += "=" * (4 - missing_padding)
        
        decoded_bytes = base64.b64decode(base64_str)
        number = int.from_bytes(decoded_bytes, "big")
        
        return from_base_10(number, to_base)
    except Exception:
        return None
