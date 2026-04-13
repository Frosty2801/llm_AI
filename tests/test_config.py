# Tests for configuration loading.

import os
import pytest
from unittest.mock import patch
from src.models import get_required_env_var


class TestEnvironmentVariables:
    """Test environment variable handling."""

    def test_get_required_env_var_success(self):
        """Test successful retrieval of required env var."""
        with patch.dict(os.environ, {"TEST_VAR": "test_value"}):
            result = get_required_env_var("TEST_VAR")
            assert result == "test_value"

    def test_get_required_env_var_missing(self):
        """Test error when required env var is missing."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="Missing required environment variable: MISSING_VAR"):
                get_required_env_var("MISSING_VAR")