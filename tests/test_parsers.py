import json
from utils.parsers import parse_config, extract_values_to_search


############ parse_config ############
# 1 valid case
# 1 invalid case
def test_parse_config_valid():
    """When passed a config file, it should return true if the config is successfully parsed and the values are successfully read"""

    config = parse_config("tests/templates/config_valid.json")
    assert config["should"] == ["Sample Text"]
    assert config["shouldNot"] == ["Another Sample Text"]


def test_parse_config_invalid():
    """When passed a config file, it should return false if the config is not successfully parsed"""

    config = parse_config("tests/templates/config_invalid_json.json")
    assert config is None


############ parse_config ############
# 1 valid case
# 1 invalid case
def test_extract_values_to_search_config_valid():
    """When passed a valid config, it should return source as config with the values sucessfully extracted from the config"""

    # config with both keys
    data = {"config": "tests/templates/config_valid.json"}
    result = extract_values_to_search(data)
    assert result["source"] == "config"
    assert result["data"]["should"] == ["Sample Text"]
    assert result["data"]["shouldNot"] == ["Another Sample Text"]

    # config with a single key
    data2 = {"config": "tests/templates/config_empty_values.json"}
    result2 = extract_values_to_search(data2)
    assert result2["source"] == "config"
    assert result2["data"]["should"] == ["Sample Text"]
    assert result2["data"]["shouldNot"] == []


def test_extract_values_to_search_config_json_valid():
    """When passed a valid config, it should return source as config with the values sucessfully extracted from the config"""

    # config with both keys
    json_data = json.dumps({"config": "tests/templates/config_valid.json"})
    parsed_data = json.loads(json_data)
    result = extract_values_to_search(parsed_data)
    assert result["source"] == "config"
    assert result["data"]["should"] == ["Sample Text"]
    assert result["data"]["shouldNot"] == ["Another Sample Text"]

    # config with a single key
    json_data2 = json.dumps({"config": "tests/templates/config_empty_values.json"})
    parsed_data2 = json.loads(json_data2)
    result2 = extract_values_to_search(parsed_data2)
    assert result2["source"] == "config"
    assert result2["data"]["should"] == ["Sample Text"]
    assert result2["data"]["shouldNot"] == []


def test_extract_values_to_search_commandline_valid():
    """When passed a valid commandline, it should return source as commandline with the values sucessfully extracted from the commandline"""

    # commandline with both keys
    data = {"should": "Sample Text", "should_not": "Another Sample Text"}
    result = extract_values_to_search(data)
    assert result["source"] == "command-line arguments"
    assert result["data"]["should"] == "Sample Text"
    assert result["data"]["shouldNot"] == "Another Sample Text"

    # commandline with a single key
    data2 = {"should": "Sample Text"}
    result2 = extract_values_to_search(data2)
    assert result2["source"] == "command-line arguments"
    assert result2["data"]["should"] == "Sample Text"
    assert result2["data"]["shouldNot"] == ""


def test_extract_values_to_search_commandline_json_valid():
    """When passed a valid command-line input in JSON, it should return source as command-line with the values successfully extracted."""

    # Convert dictionary to JSON string
    json_data = json.dumps(
        {"should": "Sample Text", "should_not": "Another Sample Text"}
    )

    # Since `extract_values_to_search` expects the data in a dictionary format, we parse the JSON string back to a dictionary.
    parsed_data = json.loads(json_data)

    result = extract_values_to_search(parsed_data)
    assert result["source"] == "command-line arguments"
    assert result["data"]["should"] == "Sample Text"
    assert result["data"]["shouldNot"] == "Another Sample Text"

    # Command-line with a single key
    json_data2 = json.dumps({"should": "Sample Text"})
    parsed_data2 = json.loads(json_data2)

    result2 = extract_values_to_search(parsed_data2)
    assert result2["source"] == "command-line arguments"
    assert result2["data"]["should"] == "Sample Text"
    assert result2["data"]["shouldNot"] == ""
