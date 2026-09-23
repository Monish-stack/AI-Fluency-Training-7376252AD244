from agent import agent

QUESTION = """
Which laptop has the lowest discounted price, and what are its
RAM and storage specifications?
"""

print("=" * 72)
print("REACT AGENT")
print("=" * 72)

print("\nQUESTION:")
print(QUESTION)

print("\n--- AGENT TRACE ---")

answer = agent(QUESTION, max_steps=8)

print("\nFINAL ANSWER:")
print(answer)