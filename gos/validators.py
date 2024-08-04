"""
Valid all the input paramters passed to the script

Parameters:
1. -i <input> : Input file or directory

<input validations>:
1. Check if the input parameter is provided
2. Check if the input parameter is a valid file or directory

# TODO: Add More stuff
"""

from os.path import isfile, isdir


def exists(value: str) -> bool:
    """Checks if the value parameter exists"""
    if not value:
        return False
    return True


def valid_input(value):
    """
    Validates the input parameter passed using -i
    1. Checks if input parameter is provided
    """

    # Check if input is empty
    if not exists(value):
        return {"status": False, "message": "Error: Input parameter not provided"}

    # Check if input is a valid file or directory
    if not isfile(value) and not isdir(value):
        return {
            "status": False,
            "message": "Error: Input is not a valid file or directory",
        }

    return {"status": True, "message": "Input is valid"}


def is_input_valid(parser):
    """Validate all the input parameters passed to the script"""
    args = parser.parse_args()

    # -i <input>
    input_validation_result = valid_input(args.input)
    if not input_validation_result["status"]:
        return input_validation_result
