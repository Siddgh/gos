"""
This file hosts all the functions required for parsing different files
"""

import json
import os
from utils.tree_helper import get_files_and_directories, get_full_path, search_in_file


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
    data = []
    if should:
        data.append({"type": "should", "text": should})
    if should_not:
        data.append({"type": "shouldNot", "text": should_not})

    return {"source": "command-line arguments", "data": data}


def start_search(root, silent=False, search_string=None):
    """Wrapper file that decides if traverse_and_create_tree is required and ensures it gets all the required input parameters"""
    if search_string:
        return traverse_and_create_tree(root, silent, search_string)
    return None


def traverse_and_create_tree(root, silent=False, search_string=None):
    """Traverses the given directory and creates a tree structure"""
    tree_obj = {"name": os.path.basename(root), "type": "directory", "children": []}
    contents = get_files_and_directories(root)
    for item in contents:
        path = get_full_path(root, item)
        if os.path.isdir(path):
            child_tree = traverse_and_create_tree(path, silent, search_string)
            tree_obj["children"].append(child_tree)
        elif os.path.isfile(path):
            tree_obj["children"].append(
                {
                    "name": item,
                    "type": "file",
                    "match": search_in_file(path, search_string),
                }
            )
    return tree_obj
