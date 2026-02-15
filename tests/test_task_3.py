"""
Tests for task_3.py - Directory Tree Visualizer

Tests cover:
- Directory structure visualization
- File and directory distinction
- Nested directories
- Empty directories
- Color output verification
"""
import pytest
from pathlib import Path
import sys
from colorama import Fore

# Add parent directory to path to import task_3
sys.path.insert(0, str(Path(__file__).parent.parent / "tasks"))
from task_3 import iterate_dir


class TestIterateDir:
    """Test the iterate_dir function."""

    def test_empty_directory(self, tmp_path, capsys):
        """Test with an empty directory."""
        iterate_dir(tmp_path)
        captured = capsys.readouterr()
        # Empty directory should produce no output
        assert captured.out.strip() == ""

    def test_single_file(self, tmp_path, capsys):
        """Test with a directory containing a single file."""
        (tmp_path / "test_file.txt").write_text("content")

        iterate_dir(tmp_path)
        captured = capsys.readouterr()

        # Should show file in red
        assert "test_file.txt" in captured.out
        assert Fore.RED in captured.out

    def test_single_directory(self, tmp_path, capsys):
        """Test with a directory containing a single subdirectory."""
        (tmp_path / "subdir").mkdir()

        iterate_dir(tmp_path)
        captured = capsys.readouterr()

        # Should show directory in green
        assert "subdir" in captured.out
        assert Fore.GREEN in captured.out

    def test_mixed_files_and_directories(self, tmp_path, capsys):
        """Test with both files and directories."""
        (tmp_path / "file1.txt").write_text("content")
        (tmp_path / "dir1").mkdir()
        (tmp_path / "file2.py").write_text("code")
        (tmp_path / "dir2").mkdir()

        iterate_dir(tmp_path)
        captured = capsys.readouterr()

        # Check all items are present
        assert "file1.txt" in captured.out
        assert "file2.py" in captured.out
        assert "dir1" in captured.out
        assert "dir2" in captured.out

        # Check colors
        assert Fore.RED in captured.out  # Files
        assert Fore.GREEN in captured.out  # Directories

    def test_nested_structure(self, tmp_path, capsys):
        """Test with nested directory structure."""
        # Create structure:
        # tmp_path/
        #   ├── file1.txt
        #   └── dir1/
        #       ├── file2.txt
        #       └── dir2/
        #           └── file3.txt

        (tmp_path / "file1.txt").write_text("content")
        dir1 = tmp_path / "dir1"
        dir1.mkdir()
        (dir1 / "file2.txt").write_text("content")
        dir2 = dir1 / "dir2"
        dir2.mkdir()
        (dir2 / "file3.txt").write_text("content")

        iterate_dir(tmp_path)
        captured = capsys.readouterr()

        # Check all items are present
        assert "file1.txt" in captured.out
        assert "dir1" in captured.out
        assert "file2.txt" in captured.out
        assert "dir2" in captured.out
        assert "file3.txt" in captured.out

    def test_indentation_levels(self, tmp_path, capsys):
        """Test that indentation increases with depth."""
        # Create nested structure
        dir1 = tmp_path / "level1"
        dir1.mkdir()
        dir2 = dir1 / "level2"
        dir2.mkdir()
        (dir2 / "deep_file.txt").write_text("content")

        iterate_dir(tmp_path)
        captured = capsys.readouterr()
        lines = captured.out.split('\n')

        # Find the line with deep_file.txt and check it has indentation
        deep_file_line = [line for line in lines if "deep_file.txt" in line]
        assert len(deep_file_line) == 1
        # Should have dots for indentation (two levels deep)
        assert ".." in deep_file_line[0]

    def test_custom_indent(self, tmp_path, capsys):
        """Test with custom initial indentation."""
        (tmp_path / "file.txt").write_text("content")

        iterate_dir(tmp_path, indent=">>")
        captured = capsys.readouterr()

        # Should have custom indent
        assert ">>" in captured.out

    def test_multiple_files_in_nested_dir(self, tmp_path, capsys):
        """Test with multiple files in nested directories."""
        # Create structure:
        # tmp_path/
        #   └── project/
        #       ├── main.py
        #       ├── config.py
        #       └── utils/
        #           ├── helper.py
        #           └── parser.py

        project = tmp_path / "project"
        project.mkdir()
        (project / "main.py").write_text("code")
        (project / "config.py").write_text("code")
        utils = project / "utils"
        utils.mkdir()
        (utils / "helper.py").write_text("code")
        (utils / "parser.py").write_text("code")

        iterate_dir(tmp_path)
        captured = capsys.readouterr()

        # Check all files are listed
        assert "main.py" in captured.out
        assert "config.py" in captured.out
        assert "helper.py" in captured.out
        assert "parser.py" in captured.out
        assert "utils" in captured.out

    def test_hidden_files(self, tmp_path, capsys):
        """Test that hidden files (starting with .) are also shown."""
        (tmp_path / ".hidden_file").write_text("content")
        (tmp_path / "normal_file.txt").write_text("content")

        iterate_dir(tmp_path)
        captured = capsys.readouterr()

        # Both should be shown
        assert ".hidden_file" in captured.out
        assert "normal_file.txt" in captured.out

    def test_various_file_extensions(self, tmp_path, capsys):
        """Test with various file extensions."""
        extensions = [".txt", ".py", ".json", ".md", ".csv", ".yaml"]
        for ext in extensions:
            (tmp_path / f"file{ext}").write_text("content")

        iterate_dir(tmp_path)
        captured = capsys.readouterr()

        # All files should be shown
        for ext in extensions:
            assert f"file{ext}" in captured.out

    def test_special_characters_in_names(self, tmp_path, capsys):
        """Test with special characters in file/directory names."""
        (tmp_path / "file with spaces.txt").write_text("content")
        (tmp_path / "file-with-dashes.py").write_text("code")
        (tmp_path / "file_with_underscores.md").write_text("text")

        iterate_dir(tmp_path)
        captured = capsys.readouterr()

        assert "file with spaces.txt" in captured.out
        assert "file-with-dashes.py" in captured.out
        assert "file_with_underscores.md" in captured.out

    def test_deep_nesting(self, tmp_path, capsys):
        """Test with deeply nested structure (5 levels)."""
        current = tmp_path
        for i in range(5):
            current = current / f"level_{i}"
            current.mkdir()
        (current / "deep_file.txt").write_text("content")

        iterate_dir(tmp_path)
        captured = capsys.readouterr()

        # Check that deep file is found
        assert "deep_file.txt" in captured.out
        # Check multiple levels are shown
        for i in range(5):
            assert f"level_{i}" in captured.out


class TestMainFunction:
    """Test the main function and command-line interface."""

    def test_main_with_nonexistent_path(self, capsys, monkeypatch):
        """Test main function with non-existent path."""
        # Import main function
        from task_3 import main

        # Mock sys.argv
        monkeypatch.setattr(sys, "argv", ["task_3.py", "/nonexistent/path"])

        main()
        captured = capsys.readouterr()

        # Should show error message
        assert "Error" in captured.out or "not found" in captured.out

    def test_main_without_arguments(self, capsys, monkeypatch, tmp_path):
        """Test main function without arguments (should use current directory)."""
        from task_3 import main

        # Create a file in tmp_path
        (tmp_path / "test.txt").write_text("content")

        # Change to tmp_path and run
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(sys, "argv", ["task_3.py"])

        main()
        captured = capsys.readouterr()

        # Should show the file from current directory
        assert "test.txt" in captured.out
