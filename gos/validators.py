"""
Valid all the input paramters passed to the script

Parameters:
1. -i <input> : Input file or directory

<input validations>:
1. Check if the input parameter is provided
2. Check if the input parameter is a valid file or directory
3. Check if the config (-c) file is provided with -y (should have) and -n (should not have)
4. Check if the config (-c) file is a valid json file
5. Check if the config (-c) file has all the required keys
7. Check if the inline parameters (-y, -n) are valid strings
"""

from os.path import isfile, isdir
from utils.text_formatters import remove_white_spaces
from utils.parsers import parse_config


def exists(value: str) -> bool:
    """Checks if the value parameter exists"""
    value = str(value) if value else None
    if not value or not remove_white_spaces(value):
        return False
    return True


def validate_input(value: str) -> dict:
    """
    Validates the input parameter passed using -i
    1. Checks if input parameter is provided
    2. Checks if input parameter is a valid file or directory
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

    return {"status": True, "message": "Success: Input is valid"}


def validate_config(
    config_path: str = None, should_path: str = None, should_not_path: str = None
) -> dict:
    """
    Validates the config parameter passed using -c
    1. Check if config (-c) is provided with -y (should have) and -n (should not have)
    2. Check if config (-c) is a valid json file
    3. Check if config (-c) has all the reequired keys
    """

    try:
        # Check if inline parameters are provided with the config files
        if (exists(should_path) or exists(should_not_path)) and not exists(config_path):
            return {
                "status": True,
                "message": "No Config Provided",
            }

        if (
            not exists(should_path)
            and not exists(should_not_path)
            and not exists(config_path)
        ):
            return {
                "status": False,
                "message": "Error: No parameters provided",
            }

        if exists(config_path) and (exists(should_path) or exists(should_not_path)):
            return {
                "status": False,
                "message": "Error: Both a configuration file and inline values cannot be provided simultaneously",
            }

        # Check if config file provided is a file
        if not isfile(config_path):
            return {"status": False, "message": "Error: Config file does not exist"}

        # Check if config file provided is a valid json file
        if not config_path.lower().endswith(".json"):
            return {
                "status": False,
                "message": "Error: The configuration file should be a JSON file",
            }

        # Check if config file has all the required keys
        config = parse_config(config_path)

        # Check if config file has a valid key inside
        required_types = {"should", "shouldNot"}

        # Extract the types from the configuration
        config_types = {item.get("type") for item in config}

        # Check if any required type is missing
        if not required_types.intersection(config_types):
            return {
                "status": False,
                "message": "Error: The configuration file must contain either 'should' or 'shouldNot' keys",
            }

        return {"status": True, "message": "Success: Config file is valid"}
    except TypeError:
        return {"status": False, "message": "Error: Invalid config file"}


def validate_inline_parameters(
    config: str = None, should: str = None, should_not: str = None
) -> dict:
    """Validate the inline parameters passed using -y and -n"""
    if (not exists(should) and not exists(should_not)) and not exists(config):
        return {"status": False, "message": "Error: Inline parameters are not provided"}

    return {"status": True, "message": "Success: Inline parameters are valid"}


def is_input_valid(args: any) -> dict:
    """Validate all the input parameters passed to the script"""
    try:
        # -i <input>
        input_validation_result = validate_input(args.get("input", ""))
        if not input_validation_result["status"]:
            return input_validation_result

        # -c <config>
        config_validation_result = validate_config(
            args.get("config", ""), args.get("should", ""), args.get("should_not", "")
        )
        if not config_validation_result["status"]:
            return config_validation_result

        # -y <should>> and -n <should_not>
        should_validation_result = validate_inline_parameters(
            args.get("config", ""), args.get("should", ""), args.get("should_not", "")
        )
        if not should_validation_result["status"]:
            return should_validation_result

        return {"status": True, "message": "Success: All inputs are valid"}
    except AttributeError:
        return {"status": False, "message": "Error: Invalid input parameters"}
