"""Includes test cases for all the functions at /utils/parsers.py """

from utils.parsers import parse_config, extract_values_to_search, start_search


############ parse_config ############
# 1 valid case
# 1 invalid case
def test_parse_config_valid():
    """When passed a config file, it should return true if the config is successfully parsed and the values are successfully read"""

    config = parse_config("tests/templates/config_valid.json")
    assert config == [
        {"type": "should", "text": "Sample Text"},
        {"type": "shouldNot", "text": "Another Sample Text"},
    ]


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
    assert result["data"] == [
        {"type": "should", "text": "Sample Text"},
        {"type": "shouldNot", "text": "Another Sample Text"},
    ]

    # config with a single key
    result2 = extract_values_to_search(
        config="tests/templates/config_empty_values.json"
    )
    assert result2["source"] == "config"
    assert result2["data"] == [{"type": "should", "text": "Sample Text"}]


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


############ start_search ############
# 1 valid case
# 3 invalid case


def test_start_search_with_no_parameters():
    """When passed no parameters to start search, it should return nothing"""
    result = start_search("")
    assert result is None


def test_start_search_with_no_root_and_search_string():
    """When passed no root and search string, it should return nothing"""
    result = start_search("", "Sample Text")
    assert result is None


def test_start_search_with_root_and_no_search_string():
    """When passed root and no search string, it should return nothing"""
    result = start_search(root="tests/templates")
    assert result is None


def test_start_search_with_root_and_search_string():
    """When passed root and search string, it should return the correct result"""
    result = start_search(
        root="tests/templates/",
        search_string=[{"type": "should", "text": "Sample Key"}],
    )

    expected_result = {
        "name": "",
        "type": "directory",
        "children": [
            {
                "name": "config_empty_values.json",
                "type": "file",
                "match": {"status": "success", "matches": []},
            },
            {
                "name": "config_incorrect_values.json",
                "type": "file",
                "match": {"status": "success", "matches": []},
            },
            {
                "name": "config_invalid_json.json",
                "type": "file",
                "match": {"status": "success", "matches": []},
            },
            {
                "name": "config_missing_keys.json",
                "type": "file",
                "match": {
                    "status": "success",
                    "matches": [
                        {
                            "text": "Sample Key",
                            "line_number": 2,
                            "type": "should",
                            "line_content": '"key": "Sample Key"',
                        }
                    ],
                },
            },
            {
                "name": "config_valid.json",
                "type": "file",
                "match": {"status": "success", "matches": []},
            },
        ],
    }
    assert result == expected_result
