from pathlib import Path


def _parse_cat_line(line, line_number):
    """
    Parse a single cat record line from CSV format.

    Expects format: "id,name,age" where age is a numeric value.

    Args:
        line (str): CSV line to parse
        line_number (int): Line number for error reporting

    Returns:
        dict or None: Dictionary with keys 'id', 'name', 'age' if valid,
                      None if line is malformed
    """
    try:
        id, name, age = line.strip().split(",")
        return {"id": id, "name": name, "age": int(age)}
    except ValueError:
        print(
            f"Error: Line {line_number} is malformed or has wrong data, so ignored until it is fixed. "
            "Please check this line and fix its values to include them into processing."
        )
        return None


def get_cats_info(path):
    """
    Read cat information from a CSV file and return as a list of dictionaries.

    Reads a CSV file with format "id,name,age" and creates a list of cat records.
    Invalid lines are reported with their line numbers and skipped.

    Args:
        path (str): Path to the CSV file containing cat data

    Returns:
        list: List of dictionaries, each containing 'id', 'name', and 'age' keys.
              Returns empty list if file is not found or no valid records exist.
    """
    cats = []
    try:
        with Path(path).open("r") as file:
            for line_number, line in enumerate(file, start=1):
                cat = _parse_cat_line(line, line_number)
                if cat:
                    cats.append(cat)
        return cats
    except FileNotFoundError:
        print(f"Error: File {path} was not found.")
        return cats
    