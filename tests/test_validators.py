"""
Test /gos/validators.py
"""

import os
from gos.validators import (
    exists,
    validate_input,
    validate_config,
    validate_inline_parameters,
)


############ exists ############
# 2 valid cases
# 3 invalid cases
def test_exists_string_valid():
    """When passed a string to exists, it should be True"""
    assert exists("test")


def test_exists_number_valid():
    """When passed a int to exists, it should be True"""
    assert exists(123)


def test_exists_none_invalid():
    """When passed a None to exists, it should be False"""
    assert not exists(None)


def test_exists_empty_no_input_invalid():
    """When passed no input to exists, it should be False"""
    assert not exists("")


def test_exists_with_white_spaces_valid():
    """When passed a string with only white spaces to exists, it should be False"""
    assert not exists("    ")


############ validate_input() ############
# 2 valid cases
# 5 invalid cases
def test_valid_input_file_path_valid():
    """When passed a valid file path to valid_input, it should have a status true and success message"""
    result = validate_input(os.getcwd() + "/gos/validators.py")
    assert result["status"] and result["message"] == "Success: Input is valid"


def test_valid_input_directory_path_valid():
    """When passed a valid directory path to valid_input, it should have a status true and success message"""
    result = validate_input(os.getcwd() + "/gos")
    assert result["status"] and result["message"] == "Success: Input is valid"


def test_valid_input_empty_invalid():
    """When passed an empty string to valid_input, it should have a status false and error message"""
    result = validate_input("")
    assert (
        not result["status"]
        and result["message"] == "Error: Input parameter not provided"
    )


def test_valid_input_none_invalid():
    """When passed None to valid_input, it should have a status false and error message"""
    result = validate_input(None)
    assert (
        not result["status"]
        and result["message"] == "Error: Input parameter not provided"
    )


def test_valid_input_with_white_spaces_invalid():
    """When passed a string with only white spaces to valid_input, it should have a status false and error message"""
    result = validate_input("    ")
    assert (
        not result["status"]
        and result["message"] == "Error: Input parameter not provided"
    )


def test_valid_input_no_file_invalid():
    """When passed a string which is not a file on the machine, it should have a status false and error message"""
    result = validate_input("/gos/loggers.py")
    assert (
        not result["status"]
        and result["message"] == "Error: Input is not a valid file or directory"
    )


def test_valid_input_no_directory_invalid():
    """When passed a string which is not a directory on the machine, it should have a status false and error message"""
    result = validate_input("/gos/")
    assert (
        not result["status"]
        and result["message"] == "Error: Input is not a valid file or directory"
    )


########### validate_config() ############
# 1 valid cases
# 8 invalid cases
def test_valid_config_file_valid():
    """When passed a valid config file to valid_config, it should have a status true and success message"""
    args = {
        "config": f"{os.getcwd()}/tests/templates/config_valid.json",
    }
    result = validate_config(args)
    assert result["status"] and result["message"] == "Success: Config file is valid"


def test_both_config_and_inline_both_invalid():
    """When passed both config and both inline parameters to valid_config, it should have a status false and error message"""
    args = {
        "config": "/gos/config.json",
        "should": "sample text",
        "should_not": "another sample text",
    }

    result = validate_config(args)
    assert (
        not result["status"]
        and result["message"]
        == "Error: Both a configuration file and inline values cannot be provided simultaneously"
    )


def test_both_config_and_inline_one_invalid():
    """When passed both config and a single inline parameters to valid_config, it should have a status false and error message"""
    args_should = {
        "config": "/gos/config.json",
        "should": "sample text",
    }

    args_should_not = {
        "config": "/gos/config.json",
        "should": "sample text",
    }
    result_should = validate_config(args_should)
    result_should_not = validate_config(args_should_not)
    assert (
        not result_should["status"]
        and result_should["message"]
        == "Error: Both a configuration file and inline values cannot be provided simultaneously"
    )

    assert (
        not result_should_not["status"]
        and result_should_not["message"]
        == "Error: Both a configuration file and inline values cannot be provided simultaneously"
    )


def test_valid_config_file_directory_invalid():
    """When passed a directory as config, it should have a status false and error message"""
    args = {
        "config": f"{os.getcwd()}/tests/templates",
    }
    result = validate_config(args)
    assert (
        not result["status"]
        and result["message"] == "Error: Config file does not exist"
    )


def test_valid_config_file_nonjson_invalid():
    """When passed a non json file as config, it should have a status false and error message"""
    args = {
        "config": f"{os.getcwd()}/tests/test_validators.py",
    }
    result = validate_config(args)
    assert (
        not result["status"]
        and result["message"] == "Error: The configuration file should be a JSON file"
    )


def test_valid_config_file_json_invalid():
    """When passed a json file with missing keys, it should have a status as false and error message"""
    args = {
        "config": f"{os.getcwd()}/tests/templates/config_invalid_json.json",
    }
    result = validate_config(args)
    assert (
        not result["status"]
        and result["message"]
        == "Error: The configuration file is not a valid JSON file"
    )


def test_valid_config_file_json_missing_keys_invalid():
    """When passed a json file with missing keys, it should have a status as false and error message"""
    args = {
        "config": f"{os.getcwd()}/tests/templates/config_missing_keys.json",
    }
    result = validate_config(args)
    assert (
        not result["status"]
        and result["message"]
        == "Error: The configuration file must contain either 'should' or 'shouldNot' keys"
    )


def test_valid_config_file_incorrect_values_invalid():
    """When passed a json file with incorrect values, it should have a status as false and error message"""
    args = {
        "config": f"{os.getcwd()}/tests/templates/config_incorrect_values.json",
    }
    result = validate_config(args)
    assert (
        not result["status"]
        and result["message"] == "Error: 'should' should be a list, not a str"
    )


def test_valid_config_file_empty_values_invalid():
    """When passed a json file with empty values, it should have a status as false and error message"""
    args = {
        "config": f"{os.getcwd()}/tests/templates/config_empty_values.json",
    }
    result = validate_config(args)
    assert (
        not result["status"]
        and result["message"] == "Error: 'shouldNot' list should not be empty"
    )


########### validate_inline_parameters() ############
# 1 valid cases
# 3 invalid cases


def test_validate_inline_parameters_valid():
    """When passed valid inline parameters to validate_inline_parameters, it should have a status true and success message"""
    args = {
        "should": "sample text",
    }
    result = validate_inline_parameters(args)
    assert (
        result["status"] and result["message"] == "Success: Inline parameters are valid"
    )


def test_validate_inline_parameters_empty_invalid():
    """When passed valid inline parameters to validate_inline_parameters, it should have a status true and success message"""
    args = {
        "should": "",
    }
    result = validate_inline_parameters(args)
    assert (
        not result["status"]
        and result["message"] == "Error: Inline parameters are not provided"
    )


def test_validate_inline_parameters_none_invalid():
    """When passed valid inline parameters to validate_inline_parameters, it should have a status true and success message"""
    args = {"should": None}
    result = validate_inline_parameters(args)
    assert (
        not result["status"]
        and result["message"] == "Error: Inline parameters are not provided"
    )


def test_validate_inline_parameters_with_white_spaces_invalid():
    """When passed valid inline parameters to validate_inline_parameters, it should have a status true and success message"""
    args = {"should": "    "}
    result = validate_inline_parameters(args)
    assert (
        not result["status"]
        and result["message"] == "Error: Inline parameters are not provided"
    )
