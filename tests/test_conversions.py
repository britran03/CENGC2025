import pytest
from base_cracker.conversions import *

# --- Test Data ---
ASCII_STRING = "Hello, world!"
BASE64_STRING = "SGVsbG8sIHdvcmxkIQ=="
HEX_STRING = "48656c6c6f2c20776f726c6421"
BINARY_STRING = "1001000011001010110110001101100011011110010110000100000011101110110111101110010011011000110010000100001"

# --- Tests for convert_string function ---


def test_ascii_to_base64():
    """Tests converting an ASCII string to Base64."""
    assert convert_string_to_base64(ASCII_STRING) == BASE64_STRING


def test_base64_to_ascii():
    """Tests converting a Base64 string back to ASCII."""
    assert convert_base64_to_string(BASE64_STRING) == ASCII_STRING


def test_ascii_to_hex():
    """Tests converting an ASCII string to hexadecimal (base16)."""
    assert convert_string_to_number(ASCII_STRING, 16) == HEX_STRING.upper()


def test_hex_to_ascii():
    """Tests converting a hexadecimal string back to ASCII."""
    assert convert_string_(HEX_STRING, "base16", "ascii") == ASCII_STRING


def test_ascii_to_binary():
    """Tests converting an ASCII string to binary (base2)."""
    assert convert_string(ASCII_STRING, "ascii", "base2") == BINARY_STRING


def test_binary_to_ascii():
    """Tests converting a binary string back to ASCII."""
    assert convert_string(BINARY_STRING, "base2", "ascii") == ASCII_STRING


def test_base64_to_hex():
    """Tests a cross-conversion from Base64 to hexadecimal."""
    assert convert_string(BASE64_STRING, "base64", "base16") == HEX_STRING.lower()


def test_hex_to_base64():
    """Tests a cross-conversion from hexadecimal to Base64."""
    assert convert_string(HEX_STRING, "base16", "base64") == BASE64_STRING


def test_invalid_input_type():
    """Tests that an unsupported 'from_type' returns an error string."""
    result = convert_string("test", "base99", "ascii")
    assert "Error decoding" in result


def test_invalid_output_type():
    """Tests that an unsupported 'to_type' returns an error string."""
    result = convert_string("test", "ascii", "base99")
    assert "Error encoding" in result


def test_bad_base64_padding():
    """Tests that malformed Base64 input is handled gracefully."""
    result = convert_string("badb64", "base64", "ascii")
    assert "Error decoding from base64" in result


# --- Tests for helper functions ---


def test_to_base_n_invalid_base():
    """Tests that to_base_n raises ValueError for an invalid base."""
    with pytest.raises(ValueError, match="Base must be between 2 and 32"):
        to_base_n(b"test", 33)
    with pytest.raises(ValueError, match="Base must be between 2 and 32"):
        to_base_n(b"test", 1)


def test_from_base_n_invalid_base():
    """Tests that from_base_n raises ValueError for an invalid base."""
    with pytest.raises(ValueError, match="Base must be between 2 and 32"):
        from_base_n("1010", 33)
    with pytest.raises(ValueError, match="Base must be between 2 and 32"):
        from_base_n("1010", 1)


def test_zero_conversion():
    """Tests the edge case of converting the number 0."""
    assert to_base_n(b"\x00", 16) == "0"
    assert from_base_n("0", 16) == b"\x00"
