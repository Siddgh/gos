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


def extract_values_to_search(args: any) -> dict:
    """Extracts the values to search for from the provided input"""

    if isinstance(args, dict):
        config = args.get("config", None)
        should = args.get("should", None)
        should_not = args.get("should_not", None)
    else:
        config = args.config
        should = args.should
        should_not = args.should_not

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
