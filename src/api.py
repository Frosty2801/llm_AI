# API module for exposing the chat assistant via FastAPI.
# Provides REST endpoints for interacting with the LangChain assistant.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
from src.main import (
    build_runtime_messages,
    update_memory_summary,
    process_tool_calls,
    explain_topic_with_structure,
    run_tutor_session,
    answer_with_study_documents,
    list_study_documents,
)
from langchain_core.messages import HumanMessage

app = FastAPI(title="LangChain Chat Assistant", version="1.0.0")

# In-memory storage for conversations (in production, use a database)
conversations: Dict[str, Dict[str, Any]] = {}


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "LangChain Chat Assistant API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "chat": "POST /chat",
            "explain": "POST /explain",
            "tutor": "POST /tutor",
            "study": "POST /study",
            "documents": "GET /documents",
            "health": "GET /health"
        }
    }


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    tool_used: Optional[str] = None


class ExplainRequest(BaseModel):
    topic: str


class TutorRequest(BaseModel):
    topic: str


class StudyRequest(BaseModel):
    question: str


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """Main chat endpoint for general conversation with tool support."""
    conversation_id = request.conversation_id or str(uuid.uuid4())

    # Initialize conversation if new
    if conversation_id not in conversations:
        conversations[conversation_id] = {
            "messages": [],
            "memory_summary": ""
        }

    conv = conversations[conversation_id]

    # Handle special commands
    message = request.message.strip()
    if message.lower().startswith("/explain "):
        topic = message[9:].strip()
        if not topic:
            raise HTTPException(status_code=400, detail="Please provide a topic after '/explain'")
        # For special commands, we don't update conversation state
        # Just return the response
        try:
            explain_topic_with_structure(topic)
            return ChatResponse(
                response="Explanation generated (check console output)",
                conversation_id=conversation_id
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    elif message.lower() == "/explain":
        raise HTTPException(status_code=400, detail="Please provide a topic after '/explain'")

    elif message.lower().startswith("/tutor "):
        topic = message[7:].strip()
        if not topic:
            raise HTTPException(status_code=400, detail="Please provide a topic after '/tutor'")
        try:
            run_tutor_session(topic)
            return ChatResponse(
                response="Tutor session completed (check console output)",
                conversation_id=conversation_id
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    elif message.lower() == "/tutor":
        raise HTTPException(status_code=400, detail="Please provide a topic after '/tutor'")

    elif message.lower().startswith("/study "):
        question = message[7:].strip()
        if not question:
            raise HTTPException(status_code=400, detail="Please provide a question after '/study'")
        try:
            answer_with_study_documents(question)
            return ChatResponse(
                response="Study answer generated (check console output)",
                conversation_id=conversation_id
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    elif message.lower() == "/study":
        raise HTTPException(status_code=400, detail="Please provide a question after '/study'")

    elif message.lower() == "/docs":
        try:
            docs = list_study_documents.invoke({})
            return ChatResponse(
                response=f"Available documents:\n{docs}",
                conversation_id=conversation_id
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Regular chat message
    conv["messages"].append(HumanMessage(content=message))

    try:
        memory_summary, messages = process_tool_calls(conv["messages"], conv["memory_summary"])
        conv["memory_summary"] = memory_summary
        conv["messages"] = messages

        # Get the last AI response
        last_message = messages[-1] if messages else None
        response_text = last_message.content if last_message else "No response generated"

        # Check if a tool was used (simplified detection)
        tool_used = None
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            tool_used = last_message.tool_calls[0]['name']

        return ChatResponse(
            response=response_text,
            conversation_id=conversation_id,
            tool_used=tool_used
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/explain")
async def explain_endpoint(request: ExplainRequest):
    """Endpoint for structured topic explanations."""
    try:
        explain_topic_with_structure(request.topic)
        return {"message": "Explanation generated (check console output)"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tutor")
async def tutor_endpoint(request: TutorRequest):
    """Endpoint for programming tutoring sessions."""
    try:
        run_tutor_session(request.topic)
        return {"message": "Tutor session completed (check console output)"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/study")
async def study_endpoint(request: StudyRequest):
    """Endpoint for answering questions using study documents."""
    try:
        answer_with_study_documents(request.question)
        return {"message": "Study answer generated (check console output)"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents")
async def docs_endpoint():
    """Endpoint to list available study documents."""
    try:
        docs = list_study_documents.invoke({})
        return {"documents": docs.split('\n') if docs else []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation by ID."""
    if conversation_id in conversations:
        del conversations[conversation_id]
        return {"message": "Conversation deleted"}
    else:
        raise HTTPException(status_code=404, detail="Conversation not found")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}