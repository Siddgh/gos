from colorama import Fore, Style


def print_stuff(message: str, is_silent: bool = False, color: str = Fore.WHITE) -> None:
    """Global print function"""
    if is_silent:
        return
    print(color + message + Style.RESET_ALL)


def print_info(message, is_silent=False, color=Fore.WHITE):
    """Wrapper to print info message"""
    if is_silent:
        return
    print(color + message + Style.RESET_ALL)


def print_error(message: str, is_silent: bool = False) -> None:
    """Wrapper to print error message"""
    print_stuff(f"✗ {message}", is_silent, Fore.RED)


def print_success(message: str, is_silent: bool = False) -> None:
    """Wrapper to print success message"""
    print_stuff(f"✔ {message}", is_silent, Fore.GREEN)


def print_divider(is_silent=False, color=Fore.WHITE):
    """Prints a simple divider"""
    if is_silent:
        return
    print(color + "=" * 40 + Style.RESET_ALL)


def print_header_with_divider(message, is_silent=False):
    """Prints two dividers with message written in between"""
    print_divider(is_silent)
    print_info(message, is_silent)
    print_divider(is_silent)


def print_values(message, is_silent=False, color=Fore.WHITE):
    """Prints argument name and its value in args: arg1 format while highlight the argument value"""
    if is_silent:
        return

    # Split the message into parts based on the colon
    if ":" in message:
        left, right = message.split(":", 1)
        left = left.strip()  # Remove any extra spaces around the left part
        right = right.strip()  # Remove any extra spaces around the right part

        # Print with different colors for each part
        print(
            Fore.WHITE
            + left
            + Style.RESET_ALL
            + ": "
            + Fore.YELLOW
            + right
            + Style.RESET_ALL
        )
    else:
        # If no colon is present, just print the message in the specified color
        print(color + message + Style.RESET_ALL)


def print_file_tree(node, prefix="", is_last=True, show_files=False, is_silent=False):
    """Recursively prints the file tree with extended lines and match details."""
    connector = "└── " if is_last else "├── "
    vertical = "│   " if not is_last else "    "
    spacer = "    " if is_last else "│   "

    # Print the current directory or file
    if node["type"] == "directory":
        print_info(f'{prefix}{connector}{node["name"]}', is_silent)
        if "children" in node:
            # Adjust prefix for children
            new_prefix = prefix + spacer
            # Iterate over the children
            num_children = len(node["children"])
            for i, child in enumerate(node["children"]):
                # Determine if this is the last item in the list
                is_last_child = i == num_children - 1
                # Print the child with updated prefix
                print_file_tree(child, new_prefix, is_last_child, show_files, is_silent)
    elif node["type"] == "file" and show_files:
        # Get match information and determine color
        matches = node.get("match", {}).get("matches", [])
        color = Fore.YELLOW if matches else Fore.WHITE
        # Print the file name
        print_info(f'{prefix}{connector}{node["name"]}', is_silent, color=color)
        if matches:
            # Print match information
            for match in matches:
                icon = "✔" if match["type"] == "should" else "✘"
                line_content = match.get("line_content", "")
                match_line = f"{prefix}{vertical} {icon} (Line {match['line_number']}) \"{match['text']}\": {line_content}"
                match_color = Fore.GREEN if match["type"] == "should" else Fore.RED
                print_info(match_line, is_silent, color=match_color)
