"""
Tests for task_4.py - Contact Management Bot

Tests cover:
- Input parsing
- Phone validation
- Adding contacts
- Updating contacts
- Retrieving phone numbers
- Duplicate prevention
- Error handling
- Helper functions
"""
import pytest
from pathlib import Path
import sys
from colorama import Fore, Style

# Add parent directory to path to import task_4
sys.path.insert(0, str(Path(__file__).parent.parent / "tasks"))
from task_4 import (
    parse_input,
    print_error,
    print_success,
    validate_args_count,
    validate_phone_with_error,
    validate_phone,
    add_contact,
    update_contact,
    get_users_phone,
    USERS,
)


@pytest.fixture(autouse=True)
def clear_users():
    """Clear USERS dictionary before each test."""
    USERS.clear()
    yield
    USERS.clear()


class TestParseInput:
    """Test the parse_input function."""

    def test_parse_simple_command(self):
        """Test parsing a simple command."""
        command, args = parse_input("hello")
        assert command == "hello"
        assert args == []

    def test_parse_command_with_args(self):
        """Test parsing command with arguments."""
        command, args = parse_input("add Alice 1234567890")
        assert command == "add"
        assert args == ["Alice", "1234567890"]

    def test_parse_command_multiple_args(self):
        """Test parsing command with multiple arguments."""
        command, args = parse_input("change Bob 9876543210")
        assert command == "change"
        assert args == ["Bob", "9876543210"]

    def test_parse_empty_input(self):
        """Test parsing empty input (critical bug fix test)."""
        command, args = parse_input("")
        assert command == ""
        assert args == []

    def test_parse_whitespace_only(self):
        """Test parsing whitespace-only input."""
        command, args = parse_input("   ")
        assert command == ""
        assert args == []

    def test_parse_command_case_insensitive(self):
        """Test that command is converted to lowercase."""
        command, args = parse_input("HELLO")
        assert command == "hello"

    def test_parse_mixed_case_command(self):
        """Test mixed case command."""
        command, args = parse_input("AdD Alice 123")
        assert command == "add"
        assert args == ["Alice", "123"]

    def test_parse_extra_spaces(self):
        """Test parsing with extra spaces."""
        command, args = parse_input("add   Alice   1234567890")
        assert command == "add"
        assert args == ["Alice", "1234567890"]


class TestValidatePhone:
    """Test the validate_phone function."""

    def test_valid_phone_10_digits(self):
        """Test valid 10-digit phone."""
        assert validate_phone("1234567890") is True

    def test_valid_phone_15_digits(self):
        """Test valid 15-digit phone."""
        assert validate_phone("123456789012345") is True

    def test_valid_phone_with_formatting(self):
        """Test phone with formatting characters."""
        assert validate_phone("+1-234-567-8900") is True
        assert validate_phone("(123) 456-7890") is True
        assert validate_phone("123.456.7890") is True

    def test_invalid_phone_too_short(self):
        """Test phone that's too short."""
        assert validate_phone("123456789") is False

    def test_invalid_phone_too_long(self):
        """Test phone that's too long."""
        assert validate_phone("1234567890123456") is False

    def test_invalid_phone_letters(self):
        """Test phone with letters."""
        assert validate_phone("12345abcde") is False

    def test_invalid_phone_special_chars(self):
        """Test phone with invalid special characters."""
        assert validate_phone("1234567890#") is False

    def test_empty_phone(self):
        """Test empty phone number."""
        assert validate_phone("") is False


class TestValidateArgsCount:
    """Test the validate_args_count helper."""

    def test_valid_args_count(self):
        """Test with correct number of arguments."""
        result = validate_args_count(["arg1", "arg2"], 2, "Error message")
        assert result is True

    def test_invalid_args_count_too_few(self, capsys):
        """Test with too few arguments."""
        result = validate_args_count(["arg1"], 2, "Need 2 args")
        assert result is False
        captured = capsys.readouterr()
        assert "Need 2 args" in captured.out

    def test_invalid_args_count_too_many(self, capsys):
        """Test with too many arguments."""
        result = validate_args_count(["a", "b", "c"], 2, "Need 2 args")
        assert result is False
        captured = capsys.readouterr()
        assert "Need 2 args" in captured.out

    def test_empty_args_list(self, capsys):
        """Test with empty args list."""
        result = validate_args_count([], 1, "Need 1 arg")
        assert result is False


class TestValidatePhoneWithError:
    """Test the validate_phone_with_error helper."""

    def test_valid_phone_returns_true(self):
        """Test with valid phone number."""
        result = validate_phone_with_error("1234567890")
        assert result is True

    def test_invalid_phone_returns_false_and_prints(self, capsys):
        """Test with invalid phone number."""
        result = validate_phone_with_error("123")
        assert result is False
        captured = capsys.readouterr()
        assert "not matching valid format" in captured.out
        assert "123" in captured.out


class TestAddContact:
    """Test the add_contact function."""

    def test_add_valid_contact(self):
        """Test adding a valid contact."""
        result = add_contact(["Alice", "1234567890"])
        assert "Contact added" in result
        assert "Alice" in USERS
        assert USERS["Alice"] == "1234567890"

    def test_add_contact_capitalization(self):
        """Test that username is capitalized."""
        add_contact(["alice", "1234567890"])
        assert "Alice" in USERS
        assert "alice" not in USERS

    def test_add_contact_invalid_phone(self, capsys):
        """Test adding contact with invalid phone."""
        result = add_contact(["Bob", "123"])
        assert result is None
        assert "Bob" not in USERS
        captured = capsys.readouterr()
        assert "not matching valid format" in captured.out

    def test_add_contact_no_args(self, capsys):
        """Test adding contact without arguments."""
        result = add_contact([])
        assert result is None
        captured = capsys.readouterr()
        assert "Command format" in captured.out

    def test_add_contact_one_arg(self, capsys):
        """Test adding contact with only one argument."""
        result = add_contact(["Alice"])
        assert result is None
        captured = capsys.readouterr()
        assert "Command format" in captured.out

    def test_add_contact_too_many_args(self, capsys):
        """Test adding contact with too many arguments."""
        result = add_contact(["Alice", "123", "extra"])
        assert result is None

    def test_add_duplicate_contact(self, capsys):
        """Test adding a contact that already exists."""
        add_contact(["Alice", "1234567890"])
        result = add_contact(["Alice", "9999999999"])

        # Should fail and show error
        assert result is None
        assert USERS["Alice"] == "1234567890"  # Original unchanged
        captured = capsys.readouterr()
        assert "already exists" in captured.out
        assert "1234567890" in captured.out  # Shows current phone
        assert "change" in captured.out.lower()  # Suggests change command

    def test_add_contact_with_formatted_phone(self):
        """Test adding contact with formatted phone number."""
        result = add_contact(["Bob", "+1-234-567-8900"])
        assert "Contact added" in result
        assert "Bob" in USERS


class TestUpdateContact:
    """Test the update_contact function."""

    def test_update_existing_contact(self):
        """Test updating an existing contact."""
        USERS["Alice"] = "1234567890"
        result = update_contact(["Alice", "9876543210"])

        assert "Contact updated" in result
        assert USERS["Alice"] == "9876543210"

    def test_update_contact_capitalization(self):
        """Test that username lookup is case-insensitive."""
        USERS["Alice"] = "1234567890"
        update_contact(["alice", "9999999999"])
        assert USERS["Alice"] == "9999999999"

    def test_update_nonexistent_contact(self, capsys):
        """Test updating a contact that doesn't exist."""
        result = update_contact(["Bob", "1234567890"])

        assert result is None
        assert "Bob" not in USERS
        captured = capsys.readouterr()
        assert "doesn't exist" in captured.out

    def test_update_contact_invalid_phone(self, capsys):
        """Test updating with invalid phone."""
        USERS["Alice"] = "1234567890"
        result = update_contact(["Alice", "123"])

        assert result is None
        assert USERS["Alice"] == "1234567890"  # Unchanged
        captured = capsys.readouterr()
        assert "not matching valid format" in captured.out

    def test_update_contact_no_args(self, capsys):
        """Test updating without arguments."""
        result = update_contact([])
        assert result is None
        captured = capsys.readouterr()
        assert "Command format" in captured.out

    def test_update_contact_one_arg(self, capsys):
        """Test updating with only one argument."""
        result = update_contact(["Alice"])
        assert result is None


class TestGetUsersPhone:
    """Test the get_users_phone function."""

    def test_get_existing_phone(self):
        """Test getting phone for existing user."""
        USERS["Alice"] = "1234567890"
        result = get_users_phone(["Alice"])

        assert "Alice" in result
        assert "1234567890" in result

    def test_get_phone_case_insensitive(self):
        """Test that username lookup is case-insensitive (bug fix test)."""
        USERS["Alice"] = "1234567890"
        result = get_users_phone(["alice"])

        assert result is not None
        assert "Alice" in result
        assert "1234567890" in result

    def test_get_nonexistent_user(self, capsys):
        """Test getting phone for non-existent user."""
        result = get_users_phone(["Bob"])

        assert result is None
        captured = capsys.readouterr()
        assert "doesn't exist" in captured.out or "no user" in captured.out.lower()
        assert "Bob" in captured.out

    def test_get_phone_no_args(self, capsys):
        """Test getting phone without arguments."""
        result = get_users_phone([])
        assert result is None
        captured = capsys.readouterr()
        assert "Command format" in captured.out

    def test_get_phone_too_many_args(self, capsys):
        """Test getting phone with too many arguments."""
        result = get_users_phone(["Alice", "Bob"])
        assert result is None
        captured = capsys.readouterr()
        assert "Command format" in captured.out


class TestPrintHelpers:
    """Test the print helper functions."""

    def test_print_error(self, capsys):
        """Test print_error helper."""
        print_error("Test error message")
        captured = capsys.readouterr()

        assert "Test error message" in captured.out
        assert Fore.RED in captured.out
        assert Style.RESET_ALL in captured.out

    def test_print_success(self, capsys):
        """Test print_success helper."""
        print_success("Test success message")
        captured = capsys.readouterr()

        assert "Test success message" in captured.out
        assert Fore.YELLOW in captured.out
        assert Style.RESET_ALL in captured.out


class TestIntegrationScenarios:
    """Integration tests for complete workflows."""

    def test_complete_workflow(self):
        """Test a complete add-update-get workflow."""
        # Add contact
        result = add_contact(["Alice", "1234567890"])
        assert "Contact added" in result
        assert USERS["Alice"] == "1234567890"

        # Get contact
        result = get_users_phone(["Alice"])
        assert "1234567890" in result

        # Update contact
        result = update_contact(["Alice", "9876543210"])
        assert "Contact updated" in result
        assert USERS["Alice"] == "9876543210"

        # Get updated contact
        result = get_users_phone(["Alice"])
        assert "9876543210" in result

    def test_multiple_contacts(self):
        """Test managing multiple contacts."""
        add_contact(["Alice", "1111111111"])
        add_contact(["Bob", "2222222222"])
        add_contact(["Charlie", "3333333333"])

        assert len(USERS) == 3
        assert USERS["Alice"] == "1111111111"
        assert USERS["Bob"] == "2222222222"
        assert USERS["Charlie"] == "3333333333"

    def test_case_insensitivity_workflow(self):
        """Test that all operations are case-insensitive."""
        # Add with lowercase
        add_contact(["alice", "1234567890"])

        # Get with different case
        result = get_users_phone(["ALICE"])
        assert "1234567890" in result

        # Update with different case
        update_contact(["Alice", "9999999999"])
        assert USERS["Alice"] == "9999999999"

    def test_error_recovery(self, capsys):
        """Test that errors don't corrupt state."""
        # Try to add with invalid phone
        add_contact(["Alice", "123"])
        assert "Alice" not in USERS

        # Add with valid phone should work
        result = add_contact(["Alice", "1234567890"])
        assert "Contact added" in result
        assert USERS["Alice"] == "1234567890"
