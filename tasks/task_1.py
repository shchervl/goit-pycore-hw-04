from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path


def _format_number(value):
    """
    Format a numeric value to 2 decimal places using ROUND_HALF_UP rounding.

    Args:
        value: Numeric value to format (int, float, or Decimal)

    Returns:
        Decimal: Formatted value with 2 decimal places
    """
    return Decimal(value).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)


def _parse_salary_line(line, line_number):
    """
    Parse a single salary line from CSV format.

    Expects format: "name,salary" where salary is a numeric value.

    Args:
        line (str): CSV line to parse
        line_number (int): Line number for error reporting

    Returns:
        float or None: Salary value if valid, None if line is malformed
    """
    try:
        _, salary = line.strip().split(",")
        return float(salary)
    except ValueError:
        print(
            f"Error: Line {line_number} is malformed or has wrong data, so ignored until it is fixed. "
            "Please check this line and fix its values to include them into processing."
        )
        return None


def total_salary(path):
    """
    Calculate total and average salary from a CSV file.

    Reads a CSV file with format "name,salary" and calculates:
    - Total sum of all valid salaries
    - Average salary across all valid entries

    Invalid lines are reported with their line numbers and skipped.
    Missing file is reported and returns (None, None).

    Args:
        path (str): Path to the CSV file containing salary data

    Returns:
        tuple: (total_salary, average_salary) as Decimal values with 2 decimal places
               Returns (None, None) if file is not found
    """
    total = 0
    employees_count = 0

    try:
        with Path(path).open("r") as file:
            for line_number, line in enumerate(file, start=1):
                salary = _parse_salary_line(line, line_number)
                if salary is not None:
                    total += salary
                    employees_count += 1

        if employees_count == 0:
            return Decimal("0.00"), Decimal("0.00")

        return _format_number(total), _format_number(total / employees_count)
    except FileNotFoundError:
        print(f"Error: File {path} was not found.")
        return None, None
