# agent_fixed.py

from config import client, MODEL


questions = [
    "What is a library?",
    "Who wrote the book Clean Code?",
    "Is Clean Code currently available in our college library?"
]


print("=" * 60)
print("PLAIN LLM - NO TOOL")
print("=" * 60)

print(f"Model: {MODEL}")
print("=" * 60)


for question in questions:

    print("\nQuestion:")
    print(question)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    answer = response.choices[0].message.content

    print("\nAnswer:")
    print(answer)

    print("-" * 60)