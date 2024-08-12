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


def print_file_tree(directory, indent=0, is_last=True, is_silent=False, prefix=""):
    """Recursively prints the file tree with match details and icons."""
    # Define symbols for directory structure
    if indent > 0:
        current_prefix = "└── " if is_last else "├── "
        new_prefix = "    " if is_last else "│   "
    else:
        current_prefix = ""
        new_prefix = ""

    # Define icons
    folder_icon = "📁"
    file_icon = "📄"
    found_icon = "✅"
    not_found_icon = "❌"

    # Check if the current item is a directory
    if directory["type"] == "directory":
        print_info(
            f"{prefix}{current_prefix}{folder_icon} {directory['name']}",
            is_silent,
        )
        children = directory.get("children", [])
        for index, child in enumerate(children):
            # Update prefix for children
            new_prefix_str = new_prefix
            if not is_last:
                new_prefix_str += prefix
            print_file_tree(
                child,
                indent + 4,
                index == len(children) - 1,
                is_silent,
                prefix + new_prefix_str,
            )

    # If the current item is a file
    elif directory["type"] == "file":
        print_info(
            f"{prefix}{current_prefix}{file_icon} {directory['name']}", is_silent
        )
        matches = directory.get("match", {}).get("matches", [])
        if matches:
            for match in matches:
                status_icon = (
                    found_icon if match["type"] == "should" else not_found_icon
                )
                status = "Found" if match["type"] == "should" else "Not Found"
                print_info(
                    f"{prefix}{' ' * 4}{status_icon} {match['text']} (Line {match['line_number']}): {status}",
                    is_silent,
                )

    # Print a message if the type is neither directory nor file
    else:
        print_info(
            f"{prefix}{current_prefix}Unknown type: {directory['type']}", is_silent
        )
