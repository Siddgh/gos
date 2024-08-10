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
