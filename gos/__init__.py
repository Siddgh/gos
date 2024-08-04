"""
Starting point for GOS
"""

import argparse
from gos.validators import is_input_valid
from gos.loggers import print_error, print_success, print_header_with_divider


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


# def create_flags_from_input(args):

#     logger.print_header_with_divider("Configuration Summary:", args.silent)

#     if args.config:
#         if os.path.isdir(args.config):
#             raise ValueError("Config file provided is a directory, not a file.")

#     if args.file:
#         if os.path.isdir(args.file):
#             raise ValueError("File provided is a directory, not a file.")

#     if args.directory:
#         if os.path.isfile(args.directory):
#             raise ValueError("Directory provided is a file, not a directory.")

#     is_file = False
#     if args.file:
#         logger.print_values(f"Searching for string in file: {args.file}", args.silent)
#         is_file = True
#     else:
#         logger.print_values(
#             f"Searching for string in directory: {args.directory}", args.silent
#         )

#     is_inline = False
#     if args.should or args.should_not:
#         is_inline = True
#     else:
#         logger.print_values(f"Using config file: {args.config}", args.silent)

#     is_should, is_should_not = False, False
#     if args.should:
#         logger.print_values(f"Should contain: {args.should}", args.silent)
#         is_should = True

#     if args.should_not:
#         logger.print_values(f"Should not contain: {args.should_not}", args.silent)
#         is_should_not = True

#     logger.print_header(
#         "✅ Configuration details are set. Proceeding with the next steps.",
#         args.silent,
#     )
#     return {
#         "is_file": is_file,
#         "is_inline": is_inline,
#         "is_should": is_should,
#         "is_should_not": is_should_not,
#     }


def main():
    """Main Function for GOS"""
    args = parse_and_validate_input()
    validation_status = is_input_valid(args)
    if validation_status["status"]:
        print_success(validation_status["message"], args.silent)
    else:
        print_error(validation_status["message"], args.silent)

    print_header_with_divider("Running GOS with below paramters", args.silent)
    # flags_dict = create_flags_from_input(args)
    # TODO: Check for flags


if __name__ == "__main__":
    main()
