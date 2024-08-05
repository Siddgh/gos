"""
This file hosts all the functions required for parsing different files
"""

import json


def parse_config(config: str) -> any:
    """Reads the provided config file and tries to convert it to a dictionary"""
    try:
        with open(config, "r", encoding="utf-8") as config_file:
            config = json.load(config_file)
            return config
    except (json.JSONDecodeError, OSError):
        return None


def extract_values_to_search(
    config: str = None, should: str = None, should_not: str = None
) -> dict:
    """Extracts the values to search for from the provided input"""

    # If input passed through config file
    if config:
        values = parse_config(config)
        return {"source": "config", "data": values}

    # If input passed is through command-line arguments
    data = {
        "should": should if should else "",
        "shouldNot": should_not if should_not else "",
    }
    return {"source": "command-line arguments", "data": data}
