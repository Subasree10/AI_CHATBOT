
# memory.py

conversations: dict[str, list[dict[str, str]]] = {}

MAX_HISTORY_MESSAGES = 10


def get_history(conversation_id: str) -> list[dict[str, str]]:
    if conversation_id not in conversations:
        conversations[conversation_id] = []

    return conversations[conversation_id]


def add_message(conversation_id: str, role: str, content: str) -> None:
    history = get_history(conversation_id)
    history.append({
        "role": role,
        "content": content
    })


def get_context(
    conversation_id: str,
    pending_message: dict[str, str] | None = None,
) -> list[dict[str, str]]:
    history = get_history(conversation_id)
    context = history[-MAX_HISTORY_MESSAGES:]
    if pending_message is not None:
        context.append(pending_message)
    return context[-MAX_HISTORY_MESSAGES:]


def trim_history(conversation_id: str) -> None:
    history = get_history(conversation_id)
    conversations[conversation_id] = history[-MAX_HISTORY_MESSAGES:]
