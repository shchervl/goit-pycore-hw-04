"""
Directory Tree Visualizer

This module provides functionality to recursively display a directory structure
in a color-coded tree format. Directories are shown in green and files in red.

Usage:
    python task_3.py <directory_path>
"""

from pathlib import Path
import sys
from colorama import Fore


def iterate_dir(path: Path, indent: str = "") -> None:
    """
    Recursively iterate through a directory and print its structure.

    This function walks through all entries in the given directory path,
    printing directories in green and files in red with appropriate indentation
    to represent the tree structure.

    Args:
        path (Path): The directory path to iterate through.
        indent (str, optional): String used for indentation to show hierarchy.
                               Defaults to empty string. Each level adds "."

    Returns:
        None

    Raises:
        PermissionError: If access to a directory is denied.
        OSError: For other file system related errors.
    """

    for entry in path.iterdir():
        if entry.is_dir():
            print(Fore.GREEN, indent, "", entry.name)
            iterate_dir(entry, indent + ".")
        if entry.is_file():
            print(Fore.RED, indent, "", entry.name)


def main() -> None:
    """
    Main entry point for the directory tree visualizer. 

    Parses command-line arguments to get the directory path and initiates  
    the directory iteration. Handles errors gracefully by displaying  
    user-friendly error messages. 

    Command-line Arguments:   
        argv[1] (str): Path to the directory to visualize, if not specified then current directory is used
    """
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
    else:
        path = Path.cwd()
    try:
        iterate_dir(path)
    except FileNotFoundError:
        print(f"Error: Path {path} was not found.")


if __name__ == "__main__":
    main()
