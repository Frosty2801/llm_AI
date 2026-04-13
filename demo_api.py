#!/usr/bin/env python3
"""
Demo script showing how to use the LangChain Chat Assistant API.
This script demonstrates basic API usage with example requests.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def demo_api_usage():
    """Demonstrate API functionality with example requests."""

    print("🚀 LangChain Chat Assistant API Demo")
    print("=" * 50)

    # Health check
    print("\n1. Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

    # List documents
    print("\n2. List Available Documents")
    try:
        response = requests.get(f"{BASE_URL}/documents")
        print(f"Status: {response.status_code}")
        print(f"Documents: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

    # Chat example
    print("\n3. Chat Example")
    try:
        payload = {
            "message": "What tools are available?",
            "conversation_id": "demo-conversation"
        }
        response = requests.post(f"{BASE_URL}/chat", json=payload)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Conversation ID: {result['conversation_id']}")
        print(f"Response: {result['response']}")
        if result.get('tool_used'):
            print(f"Tool Used: {result['tool_used']}")
    except Exception as e:
        print(f"Error: {e}")

    # Explain endpoint
    print("\n4. Explain Endpoint")
    try:
        payload = {"topic": "Python variables"}
        response = requests.post(f"{BASE_URL}/explain", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

    # Tutor endpoint
    print("\n5. Tutor Endpoint")
    try:
        payload = {"topic": "functions"}
        response = requests.post(f"{BASE_URL}/tutor", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

    # Study endpoint
    print("\n6. Study Endpoint")
    try:
        payload = {"question": "What is LangChain?"}
        response = requests.post(f"{BASE_URL}/study", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n" + "=" * 50)
    print("✅ Demo completed! Make sure the API server is running on port 8000.")
    print("💡 Start the server with: python -m src.run_api")
    print("📚 Check the README.md for more detailed usage instructions.")


if __name__ == "__main__":
    demo_api_usage()