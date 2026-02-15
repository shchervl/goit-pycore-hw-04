"""
Tests for task_1.py - Salary Calculator

Tests cover:
- Valid salary calculations
- File not found handling
- Malformed data handling
- Empty file handling
- Edge cases (single employee, zero salaries)
"""
import pytest
from decimal import Decimal
from pathlib import Path
import sys

# Add parent directory to path to import task_1
sys.path.insert(0, str(Path(__file__).parent.parent / "tasks"))
from task_1 import total_salary, _format_number, _parse_salary_line


class TestFormatNumber:
    """Test the _format_number helper function."""

    def test_format_integer(self):
        """Test formatting an integer."""
        result = _format_number(100)
        assert result == Decimal("100.00")
        assert isinstance(result, Decimal)

    def test_format_float(self):
        """Test formatting a float."""
        result = _format_number(123.456)
        assert result == Decimal("123.46")

    def test_format_float_round_half_up(self):
        """Test ROUND_HALF_UP rounding."""
        # Note: Due to floating point precision, 123.455 as float is not exactly 123.455
        # Use string or Decimal for precise rounding tests
        result = _format_number(Decimal("123.455"))
        assert result == Decimal("123.46")

    def test_format_decimal(self):
        """Test formatting a Decimal."""
        result = _format_number(Decimal("99.999"))
        assert result == Decimal("100.00")


class TestParseSalaryLine:
    """Test the _parse_salary_line helper function."""

    def test_parse_valid_line(self):
        """Test parsing a valid CSV line."""
        result = _parse_salary_line("John Doe,5000", 1)
        assert result == 5000.0

    def test_parse_valid_line_with_decimal(self):
        """Test parsing a line with decimal salary."""
        result = _parse_salary_line("Jane Smith,3500.50", 2)
        assert result == 3500.50

    def test_parse_malformed_line_missing_comma(self, capsys):
        """Test parsing a line without comma separator."""
        result = _parse_salary_line("Invalid Line", 5)
        assert result is None
        captured = capsys.readouterr()
        assert "Line 5" in captured.out
        assert "malformed" in captured.out

    def test_parse_malformed_line_invalid_salary(self, capsys):
        """Test parsing a line with non-numeric salary."""
        result = _parse_salary_line("Bob,NotANumber", 3)
        assert result is None
        captured = capsys.readouterr()
        assert "Line 3" in captured.out


class TestTotalSalary:
    """Test the main total_salary function."""

    def test_valid_salary_file(self, tmp_path):
        """Test with a valid salary file."""
        # Create test file
        test_file = tmp_path / "salaries.txt"
        test_file.write_text("Alex Korp,3000\nNikita Borisenko,2000\nSitarama Raju,1000\n")

        total, average = total_salary(str(test_file))

        assert total == Decimal("6000.00")
        assert average == Decimal("2000.00")

    def test_file_with_decimal_salaries(self, tmp_path):
        """Test with decimal salary values."""
        test_file = tmp_path / "salaries.txt"
        test_file.write_text("Alice,2500.50\nBob,3000.75\n")

        total, average = total_salary(str(test_file))

        assert total == Decimal("5501.25")
        assert average == Decimal("2750.63")

    def test_single_employee(self, tmp_path):
        """Test with only one employee."""
        test_file = tmp_path / "salaries.txt"
        test_file.write_text("SingleEmployee,5000\n")

        total, average = total_salary(str(test_file))

        assert total == Decimal("5000.00")
        assert average == Decimal("5000.00")

    def test_empty_file(self, tmp_path):
        """Test with an empty file."""
        test_file = tmp_path / "salaries.txt"
        test_file.write_text("")

        total, average = total_salary(str(test_file))

        assert total == Decimal("0.00")
        assert average == Decimal("0.00")

    def test_file_not_found(self, capsys):
        """Test with non-existent file."""
        total, average = total_salary("nonexistent_file.txt")

        assert total is None
        assert average is None
        captured = capsys.readouterr()
        assert "File" in captured.out
        assert "not found" in captured.out

    def test_file_with_malformed_lines(self, tmp_path, capsys):
        """Test file with mix of valid and invalid lines."""
        test_file = tmp_path / "salaries.txt"
        test_file.write_text(
            "Valid Employee,3000\n"
            "Invalid Line Without Comma\n"
            "Another Valid,2000\n"
            "Bad,Salary\n"
        )

        total, average = total_salary(str(test_file))

        # Only valid lines should be counted
        assert total == Decimal("5000.00")
        assert average == Decimal("2500.00")

        # Check error messages were printed
        captured = capsys.readouterr()
        assert "Line 2" in captured.out
        assert "Line 4" in captured.out

    def test_large_salaries(self, tmp_path):
        """Test with large salary values."""
        test_file = tmp_path / "salaries.txt"
        test_file.write_text("CEO,1000000\nCTO,800000\n")

        total, average = total_salary(str(test_file))

        assert total == Decimal("1800000.00")
        assert average == Decimal("900000.00")

    def test_zero_salary(self, tmp_path):
        """Test with zero salary (edge case)."""
        test_file = tmp_path / "salaries.txt"
        test_file.write_text("Intern,0\nEmployee,5000\n")

        total, average = total_salary(str(test_file))

        assert total == Decimal("5000.00")
        assert average == Decimal("2500.00")

    def test_whitespace_handling(self, tmp_path):
        """Test that whitespace in lines is handled correctly."""
        test_file = tmp_path / "salaries.txt"
        test_file.write_text("  Employee 1,3000  \n\nEmployee 2,2000\n")

        total, average = total_salary(str(test_file))

        # Should handle whitespace gracefully
        assert total == Decimal("5000.00")
        assert average == Decimal("2500.00")
