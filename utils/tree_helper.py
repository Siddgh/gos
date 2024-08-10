"""
All functions to help with traversing and creating a search tree
"""

import os
import shutil
import subprocess


def get_folder_icon(is_last: bool) -> str:
    """Returns either of the two icon depending on if its for a file or a directory"""
    return "└── " if is_last else "├── "


def get_prefix(is_last: bool) -> str:
    """Returns either of the two icons depending on if it's for a file or a directory"""
    return "    " if is_last else "│   "


def get_files_and_directories(path: str) -> list:
    """Returns a list of files and directories in the given path"""
    try:
        return sorted(os.listdir(path))
    except NotADirectoryError:
        return []


def get_full_path(root, file_name):
    """combines the root and file_name to create full directory / file path"""
    return os.path.join(root, file_name)


def search_in_file(file_path, search_items):
    """Search for the provided strings in the file using grep and categorize them by type."""
    result = {"status": "success", "matches": []}

    # Check if the file exists
    if not os.path.exists(file_path):
        result["status"] = "failure"
        result["error"] = f"File {file_path} does not exist."
        return result

    # Check if grep is available on the system
    if not shutil.which("grep"):
        result["status"] = "failure"
        result["error"] = "grep is not available on this system."
        return result

    try:
        for item in search_items:
            search_text = item["text"]
            search_type = item["type"]

            search_result = subprocess.run(
                ["grep", "-n", search_text, file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )

            found = search_result.returncode == 0
            if found:
                for line in search_result.stdout.strip().split("\n"):
                    line_number, _ = line.split(":", 1)
                    result["matches"].append(
                        {
                            "text": search_text,
                            "line_number": int(line_number),
                            "type": search_type,
                        }
                    )

    except FileNotFoundError:
        result["status"] = "failure"
        result["error"] = f"File {file_path} was not found."
    except PermissionError:
        result["status"] = "failure"
        result["error"] = f"Permission denied for file {file_path}."
    except subprocess.CalledProcessError as e:
        result["status"] = "failure"
        result["error"] = f"Subprocess error: {e}"
    except ValueError as e:
        result["status"] = "failure"
        result["error"] = f"Value error: {e}"

    return result
