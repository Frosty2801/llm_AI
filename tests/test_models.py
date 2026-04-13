# Tests for model configuration.

import pytest
from unittest.mock import patch
import os
from src.models import VALID_DEEPSEEK_MODELS


class TestModelValidation:
    """Test model configuration and validation."""

    @patch.dict(os.environ, {
        "DEEPSEEK_API_KEY": "test_key",
        "DEEPSEEK_BASE_URL": "https://api.deepseek.com",
        "DEEPSEEK_MODEL": "deepseek-chat"
    })
    def test_valid_model_initialization(self):
        """Test successful model initialization with valid config."""
        # This would normally import and initialize the model
        # But since it requires actual API access, we'll just test the validation logic
        assert "deepseek-chat" in VALID_DEEPSEEK_MODELS
        assert "deepseek-reasoner" in VALID_DEEPSEEK_MODELS

    def test_invalid_model_validation(self):
        """Test that invalid models are rejected."""
        assert "invalid-model" not in VALID_DEEPSEEK_MODELS

    def test_valid_models_list(self):
        """Test the valid models set contains expected values."""
        expected = {"deepseek-chat", "deepseek-reasoner"}
        assert VALID_DEEPSEEK_MODELS == expected