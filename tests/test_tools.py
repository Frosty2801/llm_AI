# Tests for custom tools.

import pytest
from pathlib import Path
from src.tools import (
    add_numbers,
    multiply_numbers,
    obtain_current_date_and_time,
    read_project_file,
    list_study_documents,
    retrieve_study_context,
    _get_study_docs_directory,
)


class TestMathTools:
    """Test math utility tools."""

    def test_add_numbers(self):
        """Test addition of two numbers."""
        result = add_numbers.invoke({"a": 5.0, "b": 3.0})
        assert result == 8.0

    def test_multiply_numbers(self):
        """Test multiplication of two numbers."""
        result = multiply_numbers.invoke({"a": 4.0, "b": 2.5})
        assert result == 10.0


class TestDateTimeTool:
    """Test date/time tool."""

    def test_obtain_current_date_and_time(self):
        """Test that date/time tool returns a string."""
        result = obtain_current_date_and_time.invoke({})
        assert isinstance(result, str)
        assert "The current date and time" in result


class TestFileTools:
    """Test file reading tools."""

    def test_read_project_file_existing(self):
        """Test reading an existing file."""
        # Test reading the requirements.txt file
        result = read_project_file.invoke({"file_path": "docker/requirements.txt"})
        assert isinstance(result, str)
        assert "langchain" in result

    def test_read_project_file_nonexistent(self):
        """Test reading a nonexistent file."""
        result = read_project_file.invoke({"file_path": "nonexistent.txt"})
        assert "File not found" in result

    def test_read_project_file_outside_project(self):
        """Test reading a file outside the project directory."""
        result = read_project_file.invoke({"file_path": "../../../etc/passwd"})
        assert "Access denied" in result


class TestDocumentTools:
    """Test document retrieval tools."""

    def test_list_study_documents(self):
        """Test listing study documents."""
        result = list_study_documents.invoke({})
        assert isinstance(result, str)
        # Should contain the document names we know exist
        assert "langchain_fundamentals.md" in result or "project_study_guide.md" in result

    def test_retrieve_study_context(self):
        """Test retrieving study context with a query."""
        result = retrieve_study_context.invoke({"query": "langchain"})
        assert isinstance(result, str)
        # Should return relevant sections or no results message
        assert ("Source:" in result) or ("No relevant study context" in result)

    def test_retrieve_study_context_empty_query(self):
        """Test retrieving context with empty query."""
        result = retrieve_study_context.invoke({"query": ""})
        assert "Please provide a more specific query" in result


class TestHelperFunctions:
    """Test helper functions."""

    def test_get_study_docs_directory(self):
        """Test getting the study docs directory path."""
        path = _get_study_docs_directory()
        assert isinstance(path, Path)
        assert path.name == "docs"
        assert path.exists()