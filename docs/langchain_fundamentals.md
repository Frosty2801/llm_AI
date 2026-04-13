# LangChain Fundamentals

## What LangChain is

LangChain is a framework for building applications powered by language models.
It helps organize prompts, model calls, tools, memory, retrieval, and structured outputs.

## Core building blocks

- Models: the LLM or chat model used to generate responses.
- Prompts: instructions and context sent to the model.
- Tools: external capabilities that the model can call, such as calculators or file readers.
- Memory: techniques to preserve relevant conversation context.
- Retrieval: a way to search external documents and inject useful context into the prompt.

## Tools and agents

Tools are functions exposed to the model with a name, description, and parameters.
An agent is a system where the model can decide when to use tools to solve a task.
Agents are powerful but require careful prompt design, logging, and safeguards.

## Structured output

Structured output is useful when the application expects predictable fields instead of free-form text.
This is often implemented with a schema, such as a Pydantic model.

## Memory strategies

Short-term memory usually keeps recent messages.
Long-term memory can be approximated with summaries, vector stores, or persistent storage.
A good memory system preserves goals, preferences, decisions, and unresolved tasks.

## Retrieval-Augmented Generation

RAG combines a language model with document retrieval.
The general flow is:

1. Split documents into chunks.
2. Convert chunks into searchable representations.
3. Retrieve the most relevant chunks for a user question.
4. Generate an answer grounded in those chunks.

Simple projects can start with keyword retrieval before moving to embeddings and vector databases.

## Embeddings and vector databases

Embeddings are numeric representations of text that preserve semantic similarity.
Vector databases store embeddings and make similarity search efficient.
They are useful when keyword matching is too brittle and you need semantic retrieval.
