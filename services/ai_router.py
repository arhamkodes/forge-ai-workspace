from services.providers.gemini import generate_response as gemini_response


def generate_ai_response(
    message: str,
    provider: str = "gemini",
    system_instruction: str | None = None,
) -> str:
    if provider == "gemini":
        return gemini_response(
            message=message,
            system_instruction=system_instruction,
        )

    raise ValueError(f"Unsupported AI provider: {provider}")