import unittest
from unittest.mock import AsyncMock, patch

from fastapi import HTTPException
from google.genai.errors import ClientError

from main import ChatRequest, chat
from memory import conversations, get_history


class ChatEndpointTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        conversations.clear()

    async def test_successful_chat_saves_both_messages(self):
        request = ChatRequest(conversation_id="test", message="  Explain AI  ")

        with patch(
            "main.generate_reply",
            new=AsyncMock(return_value="AI response"),
        ) as generate_reply:
            result = await chat(request)

        self.assertEqual(result["reply"], "AI response")
        self.assertEqual(
            get_history("test"),
            [
                {"role": "user", "content": "Explain AI"},
                {"role": "assistant", "content": "AI response"},
            ],
        )
        generate_reply.assert_awaited_once_with([
            {"role": "user", "content": "Explain AI"}
        ])

    async def test_invalid_api_key_is_reported_without_saving_message(self):
        request = ChatRequest(conversation_id="test", message="Explain AI")
        error = ClientError(
            400,
            {
                "error": {
                    "code": 400,
                    "message": "API key not valid",
                    "status": "INVALID_ARGUMENT",
                }
            },
        )

        with patch("main.generate_reply", new=AsyncMock(side_effect=error)):
            with self.assertRaises(HTTPException) as raised:
                await chat(request)

        self.assertEqual(raised.exception.status_code, 502)
        self.assertIn("GEMINI_API_KEY", raised.exception.detail)
        self.assertEqual(get_history("test"), [])


if __name__ == "__main__":
    unittest.main()
