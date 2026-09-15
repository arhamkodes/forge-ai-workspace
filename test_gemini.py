from services.ai_router import generate_ai_response


response = generate_ai_response(
    message="Explain what an AI agent is in two simple sentences."
)

print("\nGemini response:\n")
print(response)