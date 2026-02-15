"""
Contact Management Bot

A simple command-line bot for managing contacts with phone numbers.
Supports adding, updating, retrieving, and listing contacts with validation.
"""
import re
from colorama import Fore, Style

IDENT = " "
BOT_COLOR = Fore.YELLOW
BOT_ERROR_COLOR = Fore.RED
HELP_MAIN_TEXT=Fore.LIGHTGREEN_EX

COMMANDS_HELP_INFO = {
    "hello": f"{HELP_MAIN_TEXT}User format {BOT_COLOR}'hello' {HELP_MAIN_TEXT}just to get nice greeting :){Style.RESET_ALL}",
    "add": f"{HELP_MAIN_TEXT}Use format {BOT_COLOR}'add <username> <phone number>' {HELP_MAIN_TEXT}to add user with it's phone.'{Style.RESET_ALL}",
    "change": f"{HELP_MAIN_TEXT}Use format {BOT_COLOR}'change <username> <phone number>' {HELP_MAIN_TEXT}to update username's phone.'{Style.RESET_ALL}",
    "phone": f"{HELP_MAIN_TEXT}Use format {BOT_COLOR}'phone <username>' {HELP_MAIN_TEXT}to get phone of the user.{Style.RESET_ALL}",
    "all": f"{HELP_MAIN_TEXT}Use format {BOT_COLOR}'all' {HELP_MAIN_TEXT}to get get list of all users and their phones{Style.RESET_ALL}",
    "exit or close": f"{HELP_MAIN_TEXT}Use format {BOT_COLOR}'close' or 'exit' {HELP_MAIN_TEXT} to stop the assistant.{Style.RESET_ALL}",
}

USERS = {}


def parse_input(user_input):
    """
    Parse user input into command and arguments.
    Handles empty input gracefully.

    Returns:
        tuple: (command, args) where command is lowercase string and args is list
    """
    parts = user_input.split()
    if not parts:
        return "", []
    cmd, *args = parts
    cmd = cmd.strip().lower()
    return cmd, args


def print_error(message):
    """
    Print error message with consistent formatting.

    Args:
        message: Error message to display
    """
    print(f"{IDENT}{BOT_ERROR_COLOR}{message}{Style.RESET_ALL}")


def print_success(message):
    """
    Print success message with consistent formatting.

    Args:
        message: Success message to display
    """
    print(f"{IDENT}{BOT_COLOR}{message}{Style.RESET_ALL}")


def validate_args_count(args, expected_count, error_message):
    """
    Validate that args list has exactly expected_count items.

    Args:
        args: List of arguments to validate
        expected_count: Required number of arguments
        error_message: Message to display if validation fails

    Returns:
        bool: True if valid, False otherwise
    """
    if len(args) != expected_count:
        print_error(error_message)
        return False
    return True


def validate_phone_with_error(phone):
    """
    Validate phone format and print error if invalid.

    Args:
        phone: Phone number string to validate

    Returns:
        bool: True if valid, False otherwise
    """
    if not validate_phone(phone):
        print_error(
            f"Phone '{phone}' is not matching valid format. "
            "Should be digits only, 10 to 15 length."
        )
        return False
    return True


def print_dict_as_list(dictionary: dict):
    """
    Print dictionary items as a formatted list.

    Args:
        dictionary: Dictionary to display with key-value pairs
    """
    if not dictionary:
        print_error(f"There is no records yet.")
        return
    for key, value in dictionary.items():
        print_success(f"{key}: {value}")


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format.

    Phone must contain 10-15 digits (ignoring formatting characters
    like spaces, hyphens, parentheses, plus signs, and periods).

    Args:
        phone: Phone number string to validate

    Returns:
        bool: True if phone format is valid, False otherwise
    """
    cleaned = re.sub(r"[\s\-\(\)\+\.]", "", phone)
    return cleaned.isdigit() and 10 <= len(cleaned) <= 15


def add_contact(args):
    """
    Add a new contact to the database.

    Validates phone format and prevents duplicate usernames.
    Username is case-insensitive (stored capitalized).

    Args:
        args: List with [username, phone]

    Returns:
        Success message or None if validation fails
    """
    if not validate_args_count(args, 2, "Command format: 'add <username> <phone>'"):
        return

    username = args[0].capitalize()
    phone = args[1]

    if not validate_phone_with_error(phone):
        return

    # Check if user already exists
    if username in USERS:
        print_error(
            f"User '{username}' already exists with phone {USERS[username]}. "
            f"Use 'change {username} <new_phone>' to update, or use a different username."
        )
        return

    USERS[username] = phone
    return f"{IDENT}{BOT_COLOR}Contact added.{Style.RESET_ALL}"


def update_contact(args):
    """
    Update existing contact's phone number.

    Validates that user exists before updating.
    Username is case-insensitive (stored capitalized).

    Args:
        args: List with [username, new_phone]

    Returns:
        Success message or None if validation fails
    """
    if not validate_args_count(args, 2, "Command format: 'change <username> <phone>'"):
        return

    username = args[0].capitalize()
    phone = args[1]

    if not validate_phone_with_error(phone):
        return

    if username not in USERS:
        print_error(f"User with username '{username}' doesn't exist")
        return

    USERS[username] = phone
    return f"{IDENT}{BOT_COLOR}Contact updated.{Style.RESET_ALL}"


def get_users_phone(args: list):
    """
    Get phone number for a specific user.

    Username is case-insensitive for lookup.

    Args:
        args: List with [username]

    Returns:
        Formatted phone number message or None if user not found
    """
    if not validate_args_count(args, 1, "Command format: 'phone <username>'"):
        return

    username = args[0].capitalize()
    phone = USERS.get(username)

    if not phone:
        print_error(f"User with username '{username}' doesn't exist.")
        return

    return f"{IDENT}{BOT_COLOR}{username}'s phone is {phone}{Style.RESET_ALL}"


def main():
    """
    Main application loop for the contact management bot.

    Handles user input, routes commands, and provides interactive feedback.
    Supports commands: hello, add, change, phone, all, help, close/exit
    """
    print(f"{BOT_COLOR}Welcome to the assistant bot!{Style.RESET_ALL}")

    # Command dictionary for cleaner routing
    commands = {
        "hello": lambda args: print_success("How can I help you?"),
        "add": add_contact,
        "change": update_contact,
        "phone": get_users_phone,
        "all": lambda args: print_dict_as_list(USERS),
        "help": lambda args: print_dict_as_list(COMMANDS_HELP_INFO),
    }

    while True:
        user_input = input("Enter a command: ").strip()
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print(f"{BOT_COLOR}Good bye!{Style.RESET_ALL}")
            break
        elif command in commands:
            result = commands[command](args)
            if result:
                print(result)
                continue
        elif command:  # Only show error if command was entered and it's invalid
            print_error("Invalid command. Please use one of the list below:")
            print_dict_as_list(COMMANDS_HELP_INFO)


if __name__ == "__main__":
    main()
