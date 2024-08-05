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

    # If input passed through config file
    if args.config:
        config = parse_config(args.config)
        return {"source": "config", "data": config}

    # If input passed is through command-line arguments
    data = {
        "should": args.should if args.should else "",
        "shouldNot": args.should_not if args.should_not else "",
    }
    return {"source": "command-line arguments", "data": data}
