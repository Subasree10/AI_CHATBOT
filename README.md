# LearnMate – Context-Aware AI Chatbot

LearnMate is an AI-powered chatbot built using Python, FastAPI, and the Google Gemini API. It provides conversational responses while maintaining conversation history and context across multiple interactions.

The project demonstrates how to integrate a Large Language Model (LLM) API into a web application, manage multi-turn conversations, handle API errors, and securely manage API credentials.

## 1. Project Overview

The main objective of LearnMate is to develop a chatbot that can:

- Generate intelligent responses using the Google Gemini API.
- Maintain conversation history across multiple messages.
- Understand previous messages and use them as context.
- Follow a custom system prompt.
- Manage conversation context using a message limit.
- Handle API failures and request timeouts.
- Protect API credentials using environment variables.

## 2. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.11 | Backend programming |
| FastAPI | Backend API framework |
| Google Gemini API | AI response generation |
| Google Gen AI SDK | Communication with Gemini |
| HTML | Frontend structure |
| CSS | Frontend styling |
| JavaScript | Frontend interactions and API requests |
| python-dotenv | Environment variable management |
| Uvicorn | ASGI server |

## 3. Project Architecture

The application follows a simple frontend-backend architecture.

```text
                 USER
                   |
                   v
          index.html
       (HTML + CSS + JS)
                   |
                   v
             FastAPI
             main.py
                   |
          +--------+--------+
          |                 |
          v                 v
       memory.py          llm.py
    Conversation       Gemini API
       History          Integration
          |                 |
          |                 v
          |           Google Gemini
          |                 |
          |<----------------+
          |
          v
     Chat Response
          |
          v
       Frontend
          |
          v
         USER
```

### How It Works

1. The user enters a message in the chatbot interface.
2. JavaScript sends the message to the FastAPI backend using an HTTP POST request.
3. The backend identifies the conversation using a conversation ID.
4. The message is stored in conversation history.
5. The relevant conversation context is retrieved.
6. The backend sends the context and system prompt to the Gemini API.
7. Gemini generates a response.
8. The response is stored in conversation history.
9. FastAPI returns the response to the frontend.
10. JavaScript displays the AI-generated response.

## 4. Project Folder Structure

```text
LearnMate/
│
├── venv/
│
├── index.html
├── main.py
├── llm.py
├── memory.py
├── test_gemini.py
├── list_models.py
│
├── .env
├── .gitignore
└── requirements.txt
```

### File Descriptions

| File | Description |
|---|---|
| `index.html` | Chatbot frontend containing HTML, CSS, and JavaScript |
| `main.py` | FastAPI application and backend endpoints |
| `llm.py` | Gemini API integration and system prompt |
| `memory.py` | Conversation history and context management |
| `test_gemini.py` | Standalone Gemini API testing |
| `list_models.py` | Lists models available to the API key |
| `.env` | Stores API key and model configuration |
| `.gitignore` | Prevents sensitive and unnecessary files from being committed |
| `requirements.txt` | Lists Python dependencies |

## 5. Conversation History Management

LearnMate maintains separate conversation histories using unique conversation IDs.

A Python dictionary is used to store conversations.

Each conversation contains messages with two fields:

- `role`: Identifies whether the message is from the user or assistant.
- `content`: Contains the actual message text.

Example:

```python
conversations = {
    "conversation_1": [
        {"role": "user", "content": "What is Python?"},
        {"role": "assistant", "content": "Python is a programming language."},
        {"role": "user", "content": "What are its applications?"}
    ]
}
```

This allows Gemini to refer to earlier messages when generating responses.

**Note:** The current implementation uses in-memory storage. Conversation history is lost when the backend process restarts.

## 6. Context Window Management

To prevent unlimited conversation history from being sent to the LLM, LearnMate uses a message-based truncation strategy.

The current configuration is:

```python
MAX_HISTORY_MESSAGES = 10
```

Only the latest 10 messages are retained as conversation context.

### Benefits

- Reduces unnecessary context.
- Controls the amount of conversation history sent to Gemini.
- Helps manage API usage.
- Keeps the chatbot responsive during longer conversations.

This is a message-count limit, not an exact token-based context window.

## 7. Custom System Prompt

LearnMate uses a custom system prompt to define the chatbot's behaviour.

The system prompt instructs Gemini to act as an AI learning assistant and provide:

- Clear explanations.
- Beginner-friendly answers.
- Relevant examples.
- Structured responses.
- Helpful guidance for technical topics.

This makes the chatbot more consistent and suitable for learning-related conversations.

## 8. API Endpoints

The FastAPI backend provides the following endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Loads the chatbot frontend |
| GET | `/health` | Checks backend availability |
| GET | `/history/{conversation_id}` | Retrieves conversation history |
| POST | `/chat` | Sends a message and generates an AI response |

### POST /chat

Example request:

```json
{
    "conversation_id": "12345",
    "message": "Explain machine learning."
}
```

Example response:

```json
{
    "conversation_id": "12345",
    "reply": "Machine learning is a branch of AI..."
}
```

## 9. Error Handling

LearnMate implements error handling for common API failures.

Examples include:

- API request timeout.
- Invalid API key.
- Gemini service unavailable.
- API request failures.

User-friendly error messages are returned instead of exposing internal exceptions.

The backend also uses logging to help identify technical errors during development.

## 10. Environment Variable Management

The Gemini API key is stored in a `.env` file rather than being hardcoded into the Python source code.

Example:

```env
GEMINI_API_KEY=your_google_ai_studio_api_key
GEMINI_MODEL=your_supported_gemini_model
```

The application loads these values using `python-dotenv`.

The `.env` file is excluded from GitHub using `.gitignore` to prevent accidental exposure of API credentials.

## 11. Installation and Setup

### Prerequisites

- Python 3.11 or later.
- Google AI Studio API key.
- Visual Studio Code or another code editor.
- Internet connection.

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd LearnMate
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 4: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 5: Configure Environment Variables

Create a `.env` file in the project root directory.

Add:

```env
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=your_supported_model
```

### Step 6: Start the Backend Server

```bash
python -m uvicorn main:app --reload
```

### Step 7: Open LearnMate

Visit:

http://127.0.0.1:8000

FastAPI documentation is available at:

http://127.0.0.1:8000/docs

## 12. Requirements

The project dependencies are:

```text
fastapi
uvicorn
google-genai
python-dotenv
```

Install them using:

```bash
python -m pip install -r requirements.txt
```

## 13. Testing

The chatbot should be tested with multiple messages in the same conversation.

Example test sequence:

1. My name is Alex.
2. I am learning Python.
3. What programming language am I learning?
4. Explain variables in that language.
5. Can you give me a simple example?

The chatbot should use information from earlier messages when answering later questions.

Additional tests:

- Start a new conversation.
- Verify that separate conversations maintain separate histories.
- Test an invalid API key.
- Test API timeout handling.
- Test the health endpoint.
- Verify that the chatbot displays API errors appropriately.

## 14. Future Enhancements

Possible improvements include:

- Persistent conversation storage using SQLite or PostgreSQL.
- Token-based context management.
- Rolling conversation summaries.
- User authentication.
- Multiple conversation management.
- Improved chatbot interface.
- Markdown response rendering.
- Streaming AI responses.

## 15. Learning Outcomes

Through this project, the following concepts are demonstrated:

- Large Language Model API integration.
- Backend development using FastAPI.
- Frontend-backend communication.
- REST API development.
- Multi-turn conversational memory.
- Context window management.
- System prompt engineering.
- Environment variable management.
- API error handling.
- Python virtual environments.

## 16. Author

**Project:** LearnMate – Context-Aware AI Chatbot

**Category:** Generative AI / LLM API Integration

**Backend:** Python and FastAPI

**LLM Provider:** Google Gemini

---

*LearnMate demonstrates the integration of an external Large Language Model into a web application with conversation memory, context management, and secure API configuration.*
