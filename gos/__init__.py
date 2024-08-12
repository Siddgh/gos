"""
Starting point for GOS
"""

import argparse
import os
from gos.validators import is_input_valid
from gos.loggers import (
    print_error,
    print_success,
    print_info,
    print_values,
    print_file_tree,
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


# def traverse_and_create_tree(root, prefix="", is_last=True, silent=False):
#     """Traverses the given directory and creates a tree structure"""
#     if prefix == "":
#         # Special case for the root directory
#         print_info(os.path.basename(root), silent)
#         prefix = ""

#     icon = get_folder_icon(is_last)
#     if prefix:
#         # Only append icon if prefix is not empty, to avoid double icons at the root
#         print_info(f"{prefix}{icon}{os.path.basename(root)}", silent)
#     prefix += get_prefix(is_last)


#     contents = get_files_and_directories(root)
#     for index, item in enumerate(contents):
#         path = get_full_path(root, item)
#         is_last_item = index == len(contents) - 1
#         if os.path.isdir(path):
#             traverse_and_create_tree(path, prefix, is_last_item, silent)
#         elif os.path.isfile(path):
#             file_icon = get_folder_icon(is_last_item)
#             print_info(f"{prefix}{file_icon}{item}", silent)
def main():
    """Main Function for GOS"""
    args = parse_and_validate_input()
    validation_status = is_input_valid(args)
    if validation_status["status"]:
        print_success(validation_status["message"], args.silent)
    else:
        print_error(validation_status["message"], args.silent)

    extracted_value_result = extract_values_to_search(
        args.config, args.should, args.should_not
    )

    # should_have = extracted_value_result["data"]["should"]
    # should_not_have = extracted_value_result["data"]["shouldNot"]

    print_info(
        f"\nReading text to search from {extracted_value_result['source']}", args.silent
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
        print_values(f"Should have: {should_have}", args.silent)
    if should_not_have:
        print_values(f"Should not have: {should_not_have}", args.silent)

    # TODO: Make sure extracted_value_result["data"] is always a list
    # Currently in-line command line always returns a list, need to make sure that the elemets being returns from the config file are also returned as list.
    tree = start_search(
        root=args.input,
        silent=args.silent,
        search_string=extracted_value_result["data"],
    )
    print_file_tree(directory=tree, is_silent=args.silent)


if __name__ == "__main__":
    main()
