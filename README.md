# LangChain Chat Assistant

A comprehensive learning project demonstrating LangChain concepts including tool usage, memory management, structured output, and document retrieval.

## Features

- **Interactive Chat**: Command-line chat interface with AI assistance
- **Tool Integration**: Custom tools for math operations, file reading, and document search
- **Memory Management**: Automatic conversation summarization for long chats
- **Structured Output**: Pydantic-based formatted responses for explanations
- **Document Retrieval**: Keyword-based search over local study documents
- **REST API**: FastAPI-based endpoints for programmatic access
- **Multiple Modes**: General chat, structured explanations, tutoring, and Q&A

## Project Structure

```
├── src/
│   ├── api.py              # FastAPI endpoints
│   ├── config.py           # Environment configuration
│   ├── main.py             # Chat orchestration and CLI
│   ├── models.py           # LLM configuration
│   ├── prompts.py          # System prompts
│   ├── run_api.py          # API server entry point
│   ├── schemas.py          # Pydantic models
│   └── tools.py            # Custom tools
├── tests/                  # Unit tests
├── docs/                   # Study documents
├── docker/
│   ├── Dockerfile          # Container definition
│   ├── docker-compose.yml  # Multi-container setup
│   └── requirements.txt    # Python dependencies
└── .env.example            # Environment variables template
```

## Quick Start

### Prerequisites

- Python 3.11+
- DeepSeek API key

### Local Development

1. **Clone and setup:**
   ```bash
   git clone <repository-url>
   cd llm_AI
   cp .env.example .env
   # Edit .env with your DeepSeek API credentials
   ```

2. **Install dependencies:**
   ```bash
   pip install -r docker/requirements.txt
   ```

3. **Run the chat interface:**
   ```bash
   python -m src.main
   ```

4. **Run the API server:**
   ```bash
   python -m src.run_api
   ```

5. **Run tests:**
   ```bash
   pytest
   ```

### Docker Deployment

1. **Using Docker Compose:**
   ```bash
   cd docker
   docker-compose up --build
   ```

2. **Using Docker directly:**
   ```bash
   docker build -f docker/Dockerfile -t langchain-assistant .
   docker run -p 8000:8000 --env-file .env langchain-assistant
   ```

## API Usage

The API provides REST endpoints for all chat functionality:

### Endpoints

- `GET /health` - Health check
- `POST /chat` - General chat with tool support
- `POST /explain` - Structured topic explanations
- `POST /tutor` - Programming tutoring sessions
- `POST /study` - Q&A using study documents
- `GET /documents` - List available documents
- `DELETE /conversations/{id}` - Delete conversation

### Example API Usage

```python
import requests

# Chat endpoint
response = requests.post("http://localhost:8000/chat",
    json={"message": "What is LangChain?", "conversation_id": "optional-id"}
)
print(response.json())

# Explain endpoint
response = requests.post("http://localhost:8000/explain",
    json={"topic": "Python functions"}
)
```

### Demo Script

Run the included demo script to see all API endpoints in action:

```bash
python demo_api.py
```

This will demonstrate all the API functionality with example requests.

## Chat Commands

When using the CLI chat interface:

- `/explain <topic>` - Get structured explanation
- `/tutor <topic>` - Start tutoring session
- `/study <question>` - Ask question about study documents
- `/docs` - List available documents
- `exit` or `quit` - Exit chat

## Configuration

Set these environment variables in your `.env` file:

- `DEEPSEEK_API_KEY` - Your DeepSeek API key
- `DEEPSEEK_BASE_URL` - API base URL (default: https://api.deepseek.com)
- `DEEPSEEK_MODEL` - Model to use (deepseek-chat or deepseek-reasoner)

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_tools.py

# Run with coverage
pytest --cov=src --cov-report=html
```

### Adding New Tools

1. Define your tool function in `src/tools.py`
2. Add the `@tool` decorator
3. Include it in the `tools` list in `src/main.py`
4. Add tests in `tests/test_tools.py`

### Adding New Endpoints

1. Add endpoint in `src/api.py`
2. Update tests in `tests/test_api.py`
3. Document in this README

## Learning Path

This project demonstrates:

1. **Basic Chat Loop** - Simple conversational AI
2. **Tool Integration** - External capabilities via function calling
3. **Structured Output** - Pydantic schemas for consistent responses
4. **Memory Management** - Conversation summarization
5. **Document Retrieval** - Local knowledge base search
6. **API Development** - RESTful service with FastAPI
7. **Testing** - Unit tests for reliability
8. **Containerization** - Docker deployment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is for educational purposes.