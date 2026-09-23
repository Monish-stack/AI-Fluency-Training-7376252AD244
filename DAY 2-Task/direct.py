from config import client, MODEL, banner
from scenario import QUESTIONS

banner("DIRECT PROMPTING")

for i, question in enumerate(QUESTIONS, 1):
    print(f"\nQUESTION {i}: {question}")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0
    )

    print("\nANSWER:")
    print(response.choices[0].message.content)