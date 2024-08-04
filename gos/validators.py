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

# TODO: Add More stuff
"""

from os.path import isfile, isdir
from utils.text_formatters import remove_white_spaces
from utils.parsers import parse_config
from gos.loggers import print_stuff


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


def validate_config(args: any) -> dict:
    """
    Validates the config parameter passed using -c
    1. Check if config (-c) is provided with -y (should have) and -n (should not have)
    2. Check if config (-c) is a valid json file
    3. Check if config (-c) has all the reequired keys
    """

    # Check if inline parameters are provided with the config files
    if isinstance(args, dict):
        config_path = args.get("config", None)
        should_path = args.get("should", None)
        should_not_path = args.get("should_not", None)
    else:
        config_path = args.config
        should_path = args.should
        should_not_path = args.should_not

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
    if not config:
        return {
            "status": False,
            "message": "Error: The configuration file is not a valid JSON file",
        }

    # Check if config file has a valid key inside
    if "should" not in config or "shouldNot" not in config:
        return {
            "status": False,
            "message": "Error: The configuration file must contain either 'should' or 'shouldNot' keys",
        }

    # Check if config file has a valid value type inside
    for key in ["should", "shouldNot"]:
        if key in config:
            value = config[key]
            if not isinstance(value, list):
                return {
                    "status": False,
                    "message": f"Error: '{key}' should be a list, not a {type(value).__name__}",
                }
            if len(value) == 0:
                return {
                    "status": False,
                    "message": f"Error: '{key}' list should not be empty",
                }

    return {"status": True, "message": "Success: Config file is valid"}


def validate_inline_parameters(args: any) -> dict:
    """Validate the inline parameters passed using -y and -n"""
    if isinstance(args, dict):
        should = args.get("should", None)
        should_not = args.get("should_not", None)
        config = args.get("config", None)
    else:
        should = args.should
        should_not = args.should_not
        config = args.config

    if (not exists(should) and not exists(should_not)) and not exists(config):
        return {"status": False, "message": "Error: Inline parameters are not provided"}

    return {"status": True, "message": "Success: Inline parameters are valid"}


def is_input_valid(args: any) -> dict:
    """Validate all the input parameters passed to the script"""
    print_stuff("Validating inputs", args.silent)
    # -i <input>
    input_validation_result = validate_input(args.input)
    if not input_validation_result["status"]:
        return input_validation_result

    # -c <config>
    config_validation_result = validate_config(args)
    if not config_validation_result["status"]:
        return config_validation_result

    # -y <should>> and -n <should_not>
    should_validation_result = validate_inline_parameters(args)
    if not should_validation_result["status"]:
        return should_validation_result

    return {"status": True, "message": "Success: All inputs are valid"}
