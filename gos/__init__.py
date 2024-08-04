import argparse

# Valid Inputs
# [x] gos -d ../../sampledirectory -y 'text_to_find' -n 'text_to_avoid'
# [x] gos -f ../../samplefile.txt -y 'text_to_find' -n 'text_to_avoid'
# TODO: [ ] gos -d ../../sampledirectory -c ../../config.json
# TODO: [ ] gos -f ../../samplefile.txt -c ../../config.json
# [x] gos -d ../../sampledirectory -y 'text_to_find'
# [x] gos -f ../../samplefile.txt -y 'text_to_find'
# [x] gos -d ../../sampledirectory -n 'text_to_avoid'
# [x] gos -f ../../samplefile.txt -n 'text_to_avoid'

# Invalid Inputs
# [ ] gos -f ../../folder/ -n 'text_to_avoid' Folder instead of file
# [ ] gos -f -n 'text_to_avoid' No file


def parse_and_validate_input():
    description = "With GOS (Grep on Steriods), you can efficiently check whether certain strings exist or do not exist in your files or directories."

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-i", "--input", nargs="?", help="Input file/directory to search in"
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

    parser.add_argument("-f", "--file", nargs="?", help="File to search in")
    parser.add_argument("-d", "--directory", nargs="?", help="Directory to search in")
    parser.add_argument(
        "-c",
        "--config",
        nargs="?",
        help='JSON config file specifying "should" and "should-not" strings',
    )
    parser.add_argument(
        "-s",
        "--silent",
        action="store_true",
        help="Suppress output, returns only true/false",
    )

    # if not (args.file or args.directory):
    #     parser.error("Either file (-f) or directory (-d) is required")

    # if not (args.should or args.should_not or args.config):
    #     parser.error(
    #         "Either provide string to look for in -y (should have), -n (should not have) or -c (config json file) "
    #     )

    # if args.file and args.directory:
    #     parser.error("Only one of file (-f) or directory (-d) is allowed")

    # if (args.should and args.should_not) and args.config:
    #     parser.error(
    #         "Only one of -y (should have) or -n (should not have) or -c (config json file) is allowed"
    #     )
    return parser


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
    parser = parse_and_validate_input()
    # is_valid = validator.is_input_valid(parser)
    # flags_dict = create_flags_from_input(args)


if __name__ == "__main__":
    main()
