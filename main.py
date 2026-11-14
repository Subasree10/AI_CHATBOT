
# main.py

import asyncio
import logging
from uuid import uuid4
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from google.genai.errors import APIError
from pydantic import BaseModel, Field

from memory import (
    get_history,
    add_message,
    get_context,
    trim_history
)

from llm import generate_reply


app = FastAPI(title="LearnMate API")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent


class ChatRequest(BaseModel):

    conversation_id: str | None = None

    message: str = Field(
        min_length=1,
        max_length=4000
    )


@app.get("/")
def home():
    return FileResponse(BASE_DIR / "index.html")


@app.get("/health")
def health():
    return {"status": "LearnMate backend is running"}


@app.get("/history/{conversation_id}")
def conversation_history(conversation_id: str):
    history = get_history(conversation_id)

    return {
        "conversation_id": conversation_id,
        "messages": history
    }


@app.post("/chat")
async def chat(request: ChatRequest):

    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    conversation_id = (
        request.conversation_id or str(uuid4())
    )

    context = get_context(
        conversation_id,
        {"role": "user", "content": message},
    )

    try:
        reply = await asyncio.wait_for(
            generate_reply(context),
            timeout=180
        )

    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail="AI response timed out. Please try again."
        )

    except APIError as error:
        if error.code == 400 and "api key" in (error.message or "").lower():
            detail = (
                "Gemini rejected the API key. Update GEMINI_API_KEY in .env "
                "with a valid Google AI Studio API key."
            )
        elif error.code == 429:
            detail = (
                "Gemini API quota or rate limit reached. Check your API "
                "quota and billing, then try again."
            )
        elif error.code == 404:
            detail = (
                "Gemini model was not found. Set GEMINI_MODEL in .env to a "
                "supported model."
            )
        else:
            detail = (
                "Gemini rejected the request. Check the API configuration "
                "and try again."
            )

        logger.warning(
            "Gemini API request rejected (code=%s, status=%s)",
            error.code,
            error.status,
        )
        raise HTTPException(status_code=502, detail=detail) from error

    except Exception:
        logger.exception("Gemini API request failed")

        raise HTTPException(
            status_code=502,
            detail="AI service is temporarily unavailable. Please try again."
        )

    add_message(
        conversation_id,
        "user",
        message
    )
    add_message(
        conversation_id,
        "assistant",
        reply
    )

    trim_history(conversation_id)

    return {
        "conversation_id": conversation_id,
        "reply": reply
    }
