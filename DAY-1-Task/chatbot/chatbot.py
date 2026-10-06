import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("../.env")

api_key = os.getenv("GROQ_API_KEY")
model = os.getenv("MODEL", "openai/gpt-oss-120b")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)


def run_chatbot():
    print("\n===== PLAIN CHATBOT =====\n")

    user_request = input("User: ")

    response = client.responses.create(
        model=model,
        instructions=(
            "You are a helpful plain chatbot. "
            "Answer using only information available in the conversation. "
            "You do not have access to private files, databases, "
            "or external tools."
        ),
        input=user_request
    )

    print("\nChatbot:", response.output_text)


if __name__ == "__main__":
    run_chatbot()