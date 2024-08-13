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


def print_file_tree(directory, indent=0, is_last=True, is_silent=False):
    """Recursively prints the file tree with extended lines and match details."""
    # Define symbols for directory structure
    if indent > 0:
        prefix = "└── " if is_last else "├── "
        spacer = "    " if is_last else "│   "
        line = "│   " if not is_last else "    "
    else:
        prefix = ""
        spacer = ""
        line = ""

    # Calculate the maximum width for alignment
    max_width = 60  # Adjust this value based on your requirements
    max_line_width = (
        max_width + indent + 4
    )  # Add some padding to accommodate the tree structure

    # Check if the current item is a directory
    if directory["type"] == "directory":
        print_info(f"{' ' * indent}{prefix}{directory['name']}", is_silent)
        children = directory.get("children", [])
        for index, child in enumerate(children):
            # Recursively print each child with the appropriate prefix and spacer
            print_file_tree(child, indent + 4, index == len(children) - 1, is_silent)

    # If the current item is a file
    elif directory["type"] == "file":
        matches = directory.get("match", {}).get("matches", [])
        color = Fore.YELLOW if matches else Fore.WHITE
        print_info(f"{' ' * indent}{prefix}{directory['name']}", is_silent, color=color)
        if matches:
            for match in matches:
                status = "Found" if match["type"] == "should" else "Found"
                icon = "✔" if match["type"] == "should" else "⨯"
                line_content = match.get("line_content", "")
                color = Fore.GREEN if match["type"] == "should" else Fore.RED
                match_line = f"{' ' * (indent + 4)}{line} {icon} {status}: \"{match['text']}\" (Line {match['line_number']}): {line_content}"
                print_info(match_line.ljust(max_line_width), is_silent, color=color)
    else:
        print_info(
            f"{' ' * indent}{prefix}Unknown type: {directory['type']}", is_silent
        )
