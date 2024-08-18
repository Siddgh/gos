"""
Starting point for GOS
"""

import argparse
import os
from gos.validators import is_input_valid
from gos.loggers import (
    print_error,
    print_success,
    print_values,
    print_file_tree,
    print_header_with_divider,
    print_stuff,
)
from utils.parsers import extract_values_to_search, start_search


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

    print_stuff(os.linesep, args.silent)
    print_header_with_divider("Validating Inputs", args.silent)
    input_args = {
        "input": args.input,
        "config": args.config,
        "should": args.should,
        "should_not": args.should_not,
    }
    validation_status = is_input_valid(input_args)
    if validation_status["status"]:
        print_success(validation_status["message"], args.silent)
    else:
        print_error(validation_status["message"], args.silent)
        return

    extracted_value_result = extract_values_to_search(
        input_args.get("config", ""),
        input_args.get("should", ""),
        input_args.get("should_not", ""),
    )

    print_values(
        f"\n🔍 Searching Directory: {input_args.get('input', '')}", args.silent
    )
    print_values(
        f"🖊️  Reading search values from: {extracted_value_result['source']}",
        args.silent,
    )
    should_have = [
        item["text"]
        for item in extracted_value_result["data"]
        if item["type"] == "should"
    ]
    should_not_have = [
        item["text"]
        for item in extracted_value_result["data"]
        if item["type"] == "shouldNot"
    ]

    if should_have:
        print_values(f"└──✅ Should have: {should_have}", args.silent)
    if should_not_have:
        print_values(f"└──❌ Should not have: {should_not_have}", args.silent)

    # TODO: Make sure extracted_value_result["data"] is always a list
    # Currently in-line command line always returns a list, need to make sure that the elemets being returns from the config file are also returned as list.
    print_stuff(os.linesep, args.silent)
    print_header_with_divider("🕵️ Search Results", args.silent)
    tree = start_search(
        root=input_args.get("input", ""),
        silent=args.silent,
        search_string=extracted_value_result["data"],
    )
    print_file_tree(tree, show_files=True, is_silent=args.silent)


if __name__ == "__main__":
    main()
