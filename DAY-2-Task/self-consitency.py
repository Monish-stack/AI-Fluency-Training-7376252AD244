from config import client, MODEL, banner
from collections import Counter


QUESTION = """
Laptop A costs Rs. 60,000 with a 10% discount, while Laptop B costs
Rs. 55,000 with a 5% discount. What is the difference between their
final prices? Give only the final numerical answer in rupees.
"""


def extract_answer(text):
    """
    Extract the final numerical answer from the model response.
    """
    import re

    matches = re.findall(r"(?:Rs\.?\s*)?([\d,]+)", text)

    if matches:
        return matches[-1].replace(",", "")

    return text.strip()


# ============================================================
# NON-ZERO TEMPERATURE
# ============================================================

banner("SELF-CONSISTENCY - NON-ZERO TEMPERATURE")

print("\nQUESTION:")
print(QUESTION)

answers = []

for i in range(5):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Solve the problem carefully. "
                    "Calculate both discounted prices before finding "
                    "the difference. Give the final answer clearly."
                )
            },
            {
                "role": "user",
                "content": QUESTION
            }
        ],
        temperature=0.7
    )

    result = response.choices[0].message.content.strip()
    answer = extract_answer(result)

    answers.append(answer)

    print(f"\nRUN {i + 1}")
    print("Response:", result)
    print("Extracted answer:", answer)


# Find majority answer
counts = Counter(answers)
majority_answer, majority_count = counts.most_common(1)[0]

print("\n" + "=" * 72)
print("NON-ZERO TEMPERATURE RESULT")
print("=" * 72)

print("\nAll extracted answers:")
print(answers)

print(f"\nMajority answer: Rs. {majority_answer}")
print(f"Majority count: {majority_count}/5")

if majority_answer == "1750":
    print("Correctness: CORRECT")
else:
    print("Correctness: INCORRECT")


# ============================================================
# TEMPERATURE 0
# ============================================================

banner("SELF-CONSISTENCY - TEMPERATURE 0")

zero_answers = []

for i in range(5):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Solve the problem carefully. "
                    "Calculate both discounted prices before finding "
                    "the difference. Give the final answer clearly."
                )
            },
            {
                "role": "user",
                "content": QUESTION
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content.strip()
    answer = extract_answer(result)

    zero_answers.append(answer)

    print(f"\nRUN {i + 1}")
    print("Response:", result)
    print("Extracted answer:", answer)


print("\n" + "=" * 72)
print("TEMPERATURE 0 RESULT")
print("=" * 72)

print("\nAll extracted answers:")
print(zero_answers)

if len(set(zero_answers)) == 1:
    print("\nObservation: All five runs produced the same extracted answer.")
else:
    print("\nObservation: The runs produced different extracted answers.")