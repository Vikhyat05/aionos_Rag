from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import os
from dotenv import load_dotenv
from core.agent import get_response
from core.memory import memory
from pydantic import BaseModel

load_dotenv()

router = APIRouter()


@router.get("/ping")
async def ping():
    """
    Health check endpoint.

    Returns:
        dict: A confirmation that the server is up and running.
    """

    return {"status": "ok", "message": "Server is running!"}


@router.post("/reset_chat")
async def reset_chat(session_id: str = Query(..., description="Session ID to reset")):
    """
    Resets the chat history for a given session ID to just the system prompt.

    This is useful when the user wants to start over with a clean context.

    Args:
        session_id (str): The session identifier to reset.

    Returns:
        dict: A success message confirming the reset.
    """

    memory.clear_session(session_id)
    memory.initialize_session(session_id)
    return {
        "status": "success",
        "message": f"Chat history reset successfully for session_id: {session_id}",
    }


class ChatRequest(BaseModel):
    """
    Request schema for the /chat endpoint.

    Attributes:
        message (str): The user's message input.
        session_id (str): Unique session identifier for tracking conversation state.
    """

    message: str
    session_id: str


@router.post("/chat")
async def chat(req: ChatRequest):
    """
    Streams the assistant's response to the user's message in real time.

    This endpoint:
    - Updates the chat memory with the user message.
    - Streams the assistant's response chunk-by-chunk using Server-Sent Events (SSE).
    - Handles OpenAI function calling if triggered in the response.

    Args:
        req (ChatRequest): Contains the user's message and session ID.

    Returns:
        StreamingResponse: Text response streamed in real-time.
    """

    async def stream_from_agent():
        async for chunk in get_response(req.message, req.session_id):
            if chunk.startswith("data:"):
                try:
                    data = json.loads(chunk[len("data: ") :])
                    delta = data["choices"][0]["delta"]
                    if delta.get("content"):
                        yield delta["content"]
                except Exception as e:
                    yield f"\n[error parsing stream chunk: {e}]\n"

    return StreamingResponse(stream_from_agent(), media_type="text/plain")
