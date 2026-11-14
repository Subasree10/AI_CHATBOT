
# llm.py

import os
from collections.abc import Sequence

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
DEFAULT_MODEL = "gemini-3.8-flash"
MODEL = os.getenv("GEMINI_MODEL", "").strip()

if not API_KEY:
    raise RuntimeError("Gemini API key is missing. Set GEMINI_API_KEY in .env.")

if not MODEL or MODEL.lower() == "your_model_name":
    MODEL = DEFAULT_MODEL

client = genai.Client(api_key=API_KEY)


SYSTEM_PROMPT = """
You are LearnMate, an AI learning assistant.

Your purpose is to help students understand
programming, artificial intelligence and technology.

Rules:
1. Explain concepts in simple English.
2. Use practical examples.
3. Explain difficult technical terms.
4. Give step-by-step explanations.
5. Do not invent information.
6. Encourage understanding rather than memorisation.
"""


async def generate_reply(history: Sequence[dict[str, str]]) -> str:
    contents = []

    for message in history:
        role = "user" if message["role"] == "user" else "model"
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=message["content"])],
            )
        )

    response = await client.aio.models.generate_content(
        model=MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            max_output_tokens=800,
        ),
    )

    if not response.text or not response.text.strip():
        raise RuntimeError("Gemini returned an empty response.")

    return response.text
