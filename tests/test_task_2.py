"""
Tests for task_2.py - Cat Information Reader

Tests cover:
- Valid cat data parsing
- File not found handling
- Malformed data handling
- Empty file handling
- Edge cases (various age values, special characters)
"""
import pytest
from pathlib import Path
import sys

# Add parent directory to path to import task_2
sys.path.insert(0, str(Path(__file__).parent.parent / "tasks"))
from task_2 import get_cats_info, _parse_cat_line


class TestParseCatLine:
    """Test the _parse_cat_line helper function."""

    def test_parse_valid_line(self):
        """Test parsing a valid cat record."""
        result = _parse_cat_line("60b90c1c13067a15887e1ae1,Tayson,3", 1)
        assert result == {"id": "60b90c1c13067a15887e1ae1", "name": "Tayson", "age": 3}

    def test_parse_valid_line_different_data(self):
        """Test parsing another valid cat record."""
        result = _parse_cat_line("60b90c2413067a15887e1ae2,Vika,1", 2)
        assert result == {"id": "60b90c2413067a15887e1ae2", "name": "Vika", "age": 1}

    def test_parse_line_with_zero_age(self):
        """Test parsing a cat with age 0."""
        result = _parse_cat_line("abc123,Kitten,0", 1)
        assert result == {"id": "abc123", "name": "Kitten", "age": 0}

    def test_parse_line_with_old_cat(self):
        """Test parsing an old cat."""
        result = _parse_cat_line("old123,Grandpa,20", 1)
        assert result == {"id": "old123", "name": "Grandpa", "age": 20}

    def test_parse_malformed_line_missing_fields(self, capsys):
        """Test parsing a line with missing fields."""
        result = _parse_cat_line("id,name", 5)
        assert result is None
        captured = capsys.readouterr()
        assert "Line 5" in captured.out
        assert "malformed" in captured.out

    def test_parse_malformed_line_no_commas(self, capsys):
        """Test parsing a line without comma separators."""
        result = _parse_cat_line("InvalidLine", 3)
        assert result is None
        captured = capsys.readouterr()
        assert "Line 3" in captured.out

    def test_parse_malformed_line_non_numeric_age(self, capsys):
        """Test parsing a line with non-numeric age."""
        result = _parse_cat_line("123,Fluffy,NotANumber", 7)
        assert result is None
        captured = capsys.readouterr()
        assert "Line 7" in captured.out

    def test_parse_line_with_extra_fields(self, capsys):
        """Test parsing a line with extra fields."""
        result = _parse_cat_line("id,name,5,extra,field", 2)
        assert result is None
        captured = capsys.readouterr()
        assert "Line 2" in captured.out


class TestGetCatsInfo:
    """Test the main get_cats_info function."""

    def test_valid_cats_file(self, tmp_path):
        """Test with a valid cats file."""
        test_file = tmp_path / "cats.txt"
        test_file.write_text(
            "60b90c1c13067a15887e1ae1,Tayson,3\n"
            "60b90c2413067a15887e1ae2,Vika,1\n"
            "60b90c2e13067a15887e1ae3,Barsik,2\n"
        )

        result = get_cats_info(str(test_file))

        assert len(result) == 3
        assert result[0] == {"id": "60b90c1c13067a15887e1ae1", "name": "Tayson", "age": 3}
        assert result[1] == {"id": "60b90c2413067a15887e1ae2", "name": "Vika", "age": 1}
        assert result[2] == {"id": "60b90c2e13067a15887e1ae3", "name": "Barsik", "age": 2}

    def test_single_cat(self, tmp_path):
        """Test with a file containing only one cat."""
        test_file = tmp_path / "cats.txt"
        test_file.write_text("abc123,Solo,5\n")

        result = get_cats_info(str(test_file))

        assert len(result) == 1
        assert result[0] == {"id": "abc123", "name": "Solo", "age": 5}

    def test_empty_file(self, tmp_path):
        """Test with an empty file."""
        test_file = tmp_path / "cats.txt"
        test_file.write_text("")

        result = get_cats_info(str(test_file))

        assert result == []

    def test_file_not_found(self, capsys):
        """Test with non-existent file."""
        result = get_cats_info("nonexistent_cats.txt")

        assert result == []
        captured = capsys.readouterr()
        assert "File" in captured.out
        assert "not found" in captured.out

    def test_file_with_malformed_lines(self, tmp_path, capsys):
        """Test file with mix of valid and invalid lines."""
        test_file = tmp_path / "cats.txt"
        test_file.write_text(
            "valid1,Cat1,3\n"
            "InvalidLine\n"
            "valid2,Cat2,5\n"
            "bad,Cat3,NotANumber\n"
            "valid3,Cat3,1\n"
        )

        result = get_cats_info(str(test_file))

        # Only valid lines should be included
        assert len(result) == 3
        assert result[0]["name"] == "Cat1"
        assert result[1]["name"] == "Cat2"
        assert result[2]["name"] == "Cat3"

        # Check error messages were printed
        captured = capsys.readouterr()
        assert "Line 2" in captured.out
        assert "Line 4" in captured.out

    def test_cats_with_special_names(self, tmp_path):
        """Test cats with names containing special characters."""
        test_file = tmp_path / "cats.txt"
        test_file.write_text(
            "id1,Mr. Whiskers,3\n"
            "id2,Señor Gato,5\n"
            "id3,Cat-123,2\n"
        )

        result = get_cats_info(str(test_file))

        assert len(result) == 3
        assert result[0]["name"] == "Mr. Whiskers"
        assert result[1]["name"] == "Señor Gato"
        assert result[2]["name"] == "Cat-123"

    def test_cats_with_various_ages(self, tmp_path):
        """Test cats with various age values."""
        test_file = tmp_path / "cats.txt"
        test_file.write_text(
            "id1,Kitten,0\n"
            "id2,Young,1\n"
            "id3,Adult,5\n"
            "id4,Senior,15\n"
            "id5,Ancient,25\n"
        )

        result = get_cats_info(str(test_file))

        assert len(result) == 5
        ages = [cat["age"] for cat in result]
        assert ages == [0, 1, 5, 15, 25]

    def test_whitespace_handling(self, tmp_path):
        """Test that whitespace in lines is handled correctly."""
        test_file = tmp_path / "cats.txt"
        test_file.write_text("  id1,Cat1,3  \n\nid2,Cat2,5\n")

        result = get_cats_info(str(test_file))

        # Should handle whitespace gracefully
        assert len(result) == 2

    def test_return_type(self, tmp_path):
        """Test that function returns a list."""
        test_file = tmp_path / "cats.txt"
        test_file.write_text("id1,Cat,3\n")

        result = get_cats_info(str(test_file))

        assert isinstance(result, list)
        assert all(isinstance(cat, dict) for cat in result)

    def test_dictionary_keys(self, tmp_path):
        """Test that each dictionary has correct keys."""
        test_file = tmp_path / "cats.txt"
        test_file.write_text("id1,Cat,3\n")

        result = get_cats_info(str(test_file))

        assert len(result) == 1
        cat = result[0]
        assert set(cat.keys()) == {"id", "name", "age"}
        assert isinstance(cat["id"], str)
        assert isinstance(cat["name"], str)
        assert isinstance(cat["age"], int)
