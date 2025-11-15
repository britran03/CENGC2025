import pytest
from base_cracker.conversions import *

ASCII_STRING = "Hello, world!"
BASE64_STRING = "SGVsbG8sIHdvcmxkIQ=="
HEX_STRING = "48656c6c6f2c20776f726c6421"
BINARY_STRING = "1001000011001010110110001101100011011110010110000100000011101110110111101110010011011000110010000100001"


def test_ascii_to_base64():
    assert convert_string_to_base64(ASCII_STRING) == BASE64_STRING


def test_base64_to_ascii():
    assert convert_base64_to_string(BASE64_STRING) == ASCII_STRING


def test_ascii_to_hex():
    assert convert_string_to_number(ASCII_STRING, 16) == HEX_STRING.upper()


def test_hex_to_ascii():
    assert convert_number_to_string(HEX_STRING, 16) == ASCII_STRING


def test_ascii_to_binary():
    assert convert_string_to_number(ASCII_STRING, 2) == BINARY_STRING


def test_binary_to_ascii():
    assert convert_number_to_string(BINARY_STRING, 2) == ASCII_STRING


def test_base64_to_hex():
    assert convert_number_base(BASE64_STRING, 64, 16) == HEX_STRING.upper()


def test_hex_to_base64():
    assert convert_number_base(HEX_STRING, 16, 64) == BASE64_STRING
