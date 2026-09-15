from google import genai

from config import GEMINI_API_KEY


if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from the .env file")


client = genai.Client(api_key=GEMINI_API_KEY)


def generate_response(
    message: str,
    system_instruction: str | None = None,
) -> str:
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=message,
        config={
            "system_instruction": system_instruction
            or "You are a helpful AI assistant.",
        },
    )

    return response.text or "The AI returned an empty response."