import re
from colorama import Fore, Style

IDENT = " "
BOT_COLOR = Fore.YELLOW
BOT_ERROR_COLOR = Fore.RED

COMMANDS_HELP_INFO = {
    "hello": f"User format {BOT_COLOR}'hello' {Fore.LIGHTGREEN_EX}just to get nice greeting :){Style.RESET_ALL}",
    "add": f"Use format {BOT_COLOR}'add <username> <phone number>' {Fore.LIGHTGREEN_EX}to add user with it's phone.'{Style.RESET_ALL}",
    "change": f"Use format {BOT_COLOR}'change <username> <phone number>' {Fore.LIGHTGREEN_EX}to update username's phone.'{Style.RESET_ALL}",
    "phone": f"Use format {BOT_COLOR}'phone <username>' {Fore.LIGHTGREEN_EX}to get phone of the user.{Style.RESET_ALL}",
    "all": f"Use format {BOT_COLOR}'all' {Fore.LIGHTGREEN_EX}to get get list of all users and their phoness{Style.RESET_ALL}",
    "exit or close": f"Use format {BOT_COLOR}'close' or 'exit' {Fore.LIGHTGREEN_EX} to stop the assistant.{Style.RESET_ALL}",
}

USERS = {}


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def print_dict_as_list(dictionary: dict):
    if not dictionary:
        print(f"{IDENT}{BOT_ERROR_COLOR}There is no items yet.{Style.RESET_ALL}")
        return
    for key, value in dictionary.items():
        print(f"{IDENT}{BOT_COLOR}{key}: {Fore.LIGHTGREEN_EX}{value}{Style.RESET_ALL}")


def validate_phone(phone: str) -> bool:
    """Phone must be 10+ digits (ignoring formatting characters)."""
    cleaned = re.sub(r"[\s\-\(\)\+\.]", "", phone)
    return cleaned.isdigit() and 10 <= len(cleaned) <= 15


def add_contact(args):
    if not args or len(args) < 2 or len(args) > 2:
        print(
            f"{IDENT}{BOT_ERROR_COLOR}Command's format is wrong. Please use 'help' to check list of commands{Style.RESET_ALL}"
        )
        return
    username = args[0].capitalize()
    phone = args[1]
    if not validate_phone(phone):
        print(
            f"{IDENT}{BOT_ERROR_COLOR}Phone '{phone}' is not matchng valid format. Should be digts only 10 to 15 length.{Style.RESET_ALL}"
        )
        return
    USERS[username] = phone
    return f"{IDENT}{BOT_COLOR}Contact added.{Style.RESET_ALL}"


def update_contact(args):
    if not args or len(args) < 2 or len(args) > 2:
        print(
            f"{IDENT}{BOT_ERROR_COLOR}Command's format is wrong. Please use 'help' to check list of commands{Style.RESET_ALL}"
        )
        return
    username = args[0].capitalize()
    phone = args[1]
    if not validate_phone(phone):
        print(
            f"{IDENT}{BOT_ERROR_COLOR}Phone '{phone}' is not matchng valid format.  Should be digts only 10 to 15 length.{Style.RESET_ALL}"
        )
        return
    user_record = USERS.get(username)
    if user_record:
        USERS[username] = phone
    else:
        print(
            f"{IDENT}{BOT_ERROR_COLOR}User with  username '{username}' doesn't exist{Style.RESET_ALL}"
        )
        return
    return f"{IDENT}{BOT_COLOR}Contact updated.{Style.RESET_ALL}"


def get_users_phone(args: list):
    if not args or len(args) > 1:
        print(
            f"{IDENT}{BOT_ERROR_COLOR}Command is not complete. Please use 'help' to check list of commands{Style.RESET_ALL}"
        )
        return
    if args and args[0]:
        phone = USERS.get(args[0])
        if not phone:
            print(
                f"{IDENT}{BOT_COLOR}There is no user wiht name {str(args[0]).capitalize()}{Style.RESET_ALL}"
            )
            return
    return f"{IDENT}{BOT_COLOR}{args[0]}'s phone is {phone}{Style.RESET_ALL}"


def main():
    print(f"{BOT_COLOR}Welcome to the assistant bot!{Style.RESET_ALL}")
    while True:
        user_input = input("Enter a command: ").strip().casefold()
        command, *args = parse_input(user_input)
        if command in ["close", "exit"]:
            print(f"{BOT_COLOR}Good bye!{Style.RESET_ALL}")
            break
        elif command == "hello":
            print(f"{IDENT}{BOT_ERROR_COLOR}How can I help you?{Style.RESET_ALL}")
        elif "add" == command:
            print(add_contact(args))
        elif "change" == command:
            print(update_contact(args))
        elif "phone" == command:
            print(get_users_phone(args))
        elif command == "all":
            print_dict_as_list(USERS)
        elif command == "help":
            print_dict_as_list(COMMANDS_HELP_INFO)
        else:
            print(
                f"{IDENT}{BOT_ERROR_COLOR}Invalid command.Please use 'help' to check list of commands{Style.RESET_ALL}"
            )


if __name__ == "__main__":
    main()
