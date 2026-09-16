from services.providers.gemini import generate_response as gemini_response


def generate_ai_response(
    message: str,
    provider: str = "gemini",
    system_instruction: str | None = None,
    conversation_history: list | None = None,
) -> str:
    if provider != "gemini":
        raise ValueError(f"Unsupported AI provider: {provider}")

    history_text = ""

    if conversation_history:
        history_lines = []

        for chat_message in conversation_history:
            history_lines.append(
                f"{chat_message.role}: {chat_message.content}"
            )

        history_text = "\n".join(history_lines)

    if history_text:
        full_prompt = f"""
Here is the previous conversation:

{history_text}

Now respond to the user's latest message:

user: {message}
"""
    else:
        full_prompt = message

    return gemini_response(
        message=full_prompt,
        system_instruction=system_instruction,
    )