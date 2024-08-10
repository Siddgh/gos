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
    result = extract_values_to_search(config="tests/templates/config_valid.json")
    assert result["source"] == "config"
    assert result["data"]["should"] == ["Sample Text"]
    assert result["data"]["shouldNot"] == ["Another Sample Text"]

    # config with a single key
    result2 = extract_values_to_search(
        config="tests/templates/config_empty_values.json"
    )
    assert result2["source"] == "config"
    assert result2["data"]["should"] == ["Sample Text"]
    assert result2["data"]["shouldNot"] == []


def test_extract_values_to_search_commandline_valid():
    """When passed a valid commandline, it should return source as commandline with the values sucessfully extracted from the commandline"""

    # commandline with both keys
    result = extract_values_to_search(
        should="Sample Text", should_not="Another Sample Text"
    )
    assert result["source"] == "command-line arguments"
    assert result["data"] == [
        {"type": "should", "text": "Sample Text"},
        {"type": "shouldNot", "text": "Another Sample Text"},
    ]

    # commandline with a single key
    result2 = extract_values_to_search(should="Sample Text")
    assert result2["source"] == "command-line arguments"
    assert result2["data"] == [{"type": "should", "text": "Sample Text"}]
