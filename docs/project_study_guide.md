# Project Study Guide

## Current architecture

The project is organized into:

- `src/main.py`: chat orchestration, command handling, memory, and tool execution.
- `src/models.py`: model configuration and environment validation.
- `src/prompts.py`: reusable system prompts for each behavior.
- `src/tools.py`: external capabilities exposed to the model.
- `src/schemas.py`: structured output contracts.

## Learning path inside this project

1. Build a reliable chat loop.
2. Add multiple tools and a tool registry.
3. Introduce structured output with Pydantic.
4. Add summarized memory.
5. Create a tutor mode with more guided teaching.
6. Add a local document base and retrieval.
7. Later, move from keyword retrieval to embeddings.

## Good next improvements

- Add tests for tools and prompt-driven flows.
- Create a FastAPI endpoint for chat.
- Add logging for tool calls.
- Add retrieval over project docs with chunking.
- Replace naive retrieval with embeddings when the project grows.
