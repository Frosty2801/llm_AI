# Tests for the FastAPI endpoints.

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.api import app

client = TestClient(app)


class TestAPIEndpoints:
    """Test API endpoints."""

    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_docs_endpoint(self):
        """Test docs listing endpoint."""
        response = client.get("/documents")
        assert response.status_code == 200
        data = response.json()
        assert "documents" in data
        assert isinstance(data["documents"], list)

    @patch('src.api.explain_topic_with_structure')
    def test_explain_endpoint(self, mock_explain):
        """Test explain endpoint."""
        mock_explain.return_value = None
        response = client.post("/explain", json={"topic": "Python"})
        assert response.status_code == 200
        assert "message" in response.json()

    @patch('src.api.run_tutor_session')
    def test_tutor_endpoint(self, mock_tutor):
        """Test tutor endpoint."""
        mock_tutor.return_value = None
        response = client.post("/tutor", json={"topic": "functions"})
        assert response.status_code == 200
        assert "message" in response.json()

    @patch('src.api.answer_with_study_documents')
    def test_study_endpoint(self, mock_study):
        """Test study endpoint."""
        mock_study.return_value = None
        response = client.post("/study", json={"question": "What is LangChain?"})
        assert response.status_code == 200
        assert "message" in response.json()

    def test_chat_endpoint_special_commands(self):
        """Test chat endpoint with special commands."""
        # Test /docs command
        response = client.post("/chat", json={"message": "/docs"})
        assert response.status_code == 200
        data = response.json()
        assert "conversation_id" in data
        assert "Available documents" in data["response"]

    def test_chat_endpoint_invalid_explain(self):
        """Test chat endpoint with invalid explain command."""
        response = client.post("/chat", json={"message": "/explain"})
        assert response.status_code == 400
        assert "provide a topic" in response.json()["detail"]

    def test_delete_conversation_not_found(self):
        """Test deleting a nonexistent conversation."""
        response = client.delete("/conversations/nonexistent-id")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]