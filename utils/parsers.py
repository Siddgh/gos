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
