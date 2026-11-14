import asyncio
from google.genai.errors import APIError

from llm import generate_reply


async def test():
    print("Sending request to Gemini...")
    reply = await generate_reply([
        {"role": "user", "content": "Explain Python in two sentences."}
    ])

    print("Gemini response:")
    print(reply)


if __name__ == "__main__":
    try:
        asyncio.run(test())
    except APIError as error:
        if error.code == 400 and "api key" in (error.message or "").lower():
            raise SystemExit(
                "Gemini rejected the API key. Update GEMINI_API_KEY in .env "
                "with a valid Google AI Studio API key."
            ) from None
        raise