"""
All the common functions used for formatting
"""


def remove_white_spaces(text: str) -> str:
    """Remove whitespaces from the given string"""
    return "".join(text.split())
