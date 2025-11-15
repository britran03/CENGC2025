import argparse
import zipfile
import sys
import os
import base_cracker.cracker as cracker


BANNER = r"""
   ██████╗  ██████╗ ███████╗ ███████╗     ██████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗ 
 ██╔════╝ ██╔════█║ ██╔═══██╗██╔════╝    ██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
 ██║      ██║    █║ ██║   ██║█████╗      ██║     ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝
 ██║      ██║    █║ ██║   ██║██╔══╝      ██║     ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
 ╚██████╗ ╚███████║ ███████╔╝███████╗    ╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
  ╚═════╝  ╚══════╝  ╚═════╝ ╚══════╝     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

"""


def print_banner():
    print(BANNER)


def parse_args():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description="CENGC Code Breaking CLI Tool")

    # Always required
    parser.add_argument(
        "--zip",
        "-z",
        type=str,
        required=True,
        help="Path to ZIP file to attempt cracking",
    )

    # Code input requires depth (checked later)
    parser.add_argument(
        "--code", "-i", type=str, help="Code input string to process or decode"
    )

    parser.add_argument(
        "--depth",
        "-d",
        type=int,
        help="Try to find zip key using brute-forced conversions",
    )

    parser.add_argument(
        "--caesar",
        "-k",
        type=int,
        help="Shift input by a certain offset, as in the caesar cipher",
    )

    args = parser.parse_args()
    if not args.code:
        parser.error("Must provide code start with")

    return args


def validate_zip(path):
    """
    Make sure zip exists and is valid
    """
    if not os.path.exists(path):
        print(f"Zip does not exist: {path}")
        sys.exit(1)

    if not zipfile.is_zipfile(path):
        print(f"Not a zip file: {path}")
        sys.exit(1)


def main():
    print_banner()
    args = parse_args()

    validate_zip(args.zip)
    input_code = args.code

    if args.caesar:
        input_code = cracker.caesar_cipher(input_code, args.caesar)

    cracker.test_transformations(args.zip, args.code, args.depth)


if __name__ == "__main__":
    main()
