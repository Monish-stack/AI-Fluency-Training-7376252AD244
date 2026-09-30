import json

from config import client, MODEL
from my_tools import check_book_availability


# --------------------------------------------------
# Tool definition
# --------------------------------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "check_book_availability",
            "description": (
                "Checks the current availability of a book "
                "in the college library."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "book_name": {
                        "type": "string",
                        "description": "The name of the book to check."
                    }
                },
                "required": ["book_name"]
            }
        }
    }
]


# --------------------------------------------------
# Questions
# --------------------------------------------------

questions = [
    "What is a library?",
    "Who wrote the book Clean Code?",
    "Is Clean Code currently available in our college library?"
]


# --------------------------------------------------
# Run questions
# --------------------------------------------------

print("=" * 60)
print("LLM WITH ONE TOOL")
print("=" * 60)

print(f"Model: {MODEL}")
print("=" * 60)


for question in questions:

    print("\nQuestion:")
    print(question)

    messages = [
        {
            "role": "user",
            "content": question
        }
    ]

    # First ask the LLM
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    # --------------------------------------------------
    # Check whether the LLM requested a tool
    # --------------------------------------------------

    if message.tool_calls:

        print("\nTool Call:")

        # Add the assistant message containing the tool call
        messages.append(message)

        for tool_call in message.tool_calls:

            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print("Function:", function_name)
            print("Arguments:", arguments)

            # ------------------------------------------
            # Run our actual Python tool
            # ------------------------------------------

            if function_name == "check_book_availability":

                tool_result = check_book_availability(
                    arguments["book_name"]
                )

                print("\nTool Result:")
                print(tool_result)

                # Send tool result back to the LLM
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result
                    }
                )

        # ----------------------------------------------
        # Ask LLM for final answer using tool result
        # ----------------------------------------------

        final_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        final_answer = final_response.choices[0].message.content

        print("\nFinal Answer:")
        print(final_answer)

    else:

        print("\nTool Call:")
        print("No tool needed.")

        print("\nFinal Answer:")
        print(message.content)

    print("\n" + "-" * 60)