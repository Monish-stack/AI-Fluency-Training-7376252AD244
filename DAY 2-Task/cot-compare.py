from config import client, MODEL, banner
from scenario import QUESTIONS

banner("CHAIN-OF-THOUGHT COMPARISON")

for i, question in enumerate(QUESTIONS, 1):

    print("=" * 72)
    print(f"QUESTION {i}: {question}")

    print("\n--- WITHOUT CoT ---")

    response1 = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0
    )

    print(response1.choices[0].message.content)

    print("\n--- WITH REASONING ---")

    response2 = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": (
                    "Solve the problem carefully step by step. "
                    "Check the calculations before giving the final answer.\n\n"
                    + question
                )
            }
        ],
        temperature=0
    )

    print(response2.choices[0].message.content)