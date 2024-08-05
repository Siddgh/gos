"""
Starting point for GOS
"""

import argparse
from gos.validators import is_input_valid
from gos.loggers import print_error, print_success, print_info, print_values
from utils.parsers import extract_values_to_search


def parse_and_validate_input():
    """Parsing inputs"""

    description = "🔍 With GOS (Grep on Steriods), you can efficiently check whether certain strings exist or do not exist in your files or directories."

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-i", "--input", nargs="?", help="Input file/directory to search in"
    )

    parser.add_argument(
        "-c",
        "--config",
        nargs="?",
        help='JSON config file specifying "should" and "should-not" strings',
    )

    parser.add_argument(
        "-y",
        "--should",
        nargs="?",
        help="String that should exists in the given file/directory",
    )

    parser.add_argument(
        "-n",
        "--should_not",
        nargs="?",
        help="String that should not exists in the given file/directory",
    )

    parser.add_argument(
        "-s",
        "--silent",
        action="store_true",
        help="Suppress output, returns only true/false",
    )

    return parser.parse_args()


def main():
    """Main Function for GOS"""
    args = parse_and_validate_input()
    validation_status = is_input_valid(args)
    if validation_status["status"]:
        print_success(validation_status["message"], args.silent)
    else:
        print_error(validation_status["message"], args.silent)

    extracted_value_result = extract_values_to_search(args)
    should_have = extracted_value_result["data"]["should"]
    should_not_have = extracted_value_result["data"]["shouldNot"]

    print_info(
        f"\nReading text to search from {extracted_value_result['source']}", args.silent
    )

    if should_have:
        print_values(f"Should have: {should_have}", args.silent)
    if should_not_have:
        print_values(f"Should not have: {should_not_have}", args.silent)


if __name__ == "__main__":
    main()
