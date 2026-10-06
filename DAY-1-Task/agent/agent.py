import os
import json
from openai import OpenAI
from dotenv import load_dotenv

from tools import execute_tool


load_dotenv("../.env")

api_key = os.getenv("GROQ_API_KEY")
model = os.getenv("MODEL", "openai/gpt-oss-120b")


client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_student_information",
            "description": "Get private information about the student.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_courses",
            "description": "Get all courses, fees, deadlines, and payment statuses from the student's private data.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_course_by_name",
            "description": "Find a specific course using its name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_name": {
                        "type": "string",
                        "description": "The exact or approximate course name."
                    }
                },
                "required": ["course_name"]
            }
        }
    }
]


def run_agent(user_request):

    messages = [
        {
            "role": "system",
            "content": (
                "You are a student information AI agent. "
                "You can access private student data only through the available tools. "
                "When the user's request requires private information, use the appropriate tool. "
                "Analyze the tool results and continue working until you can provide a complete answer. "
                "Do not invent private information."
            )
        },
        {
            "role": "user",
            "content": user_request
        }
    ]

    max_iterations = 5

    for iteration in range(max_iterations):

        print(f"\n--- Agent Loop {iteration + 1} ---")

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        messages.append(assistant_message)

        # Check whether the model wants to use a tool
        if assistant_message.tool_calls:

            for tool_call in assistant_message.tool_calls:

                tool_name = tool_call.function.name

                try:
                    arguments = json.loads(
                        tool_call.function.arguments
                    )
                except json.JSONDecodeError:
                    arguments = {}

                print(f"Agent selected tool: {tool_name}")

                tool_result = execute_tool(
                    tool_name,
                    arguments
                )

                print("Tool executed successfully.")

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_name,
                        "content": json.dumps(tool_result)
                    }
                )

            # Continue the loop so the LLM can analyze
            # the tool result.
            continue

        # No tool call means the agent has finished.
        print("\n===== FINAL AGENT RESPONSE =====")
        print(assistant_message.content)

        return


    print("\nAgent stopped after maximum iterations.")


if __name__ == "__main__":

    print("\n===== AI AGENT =====\n")

    user_request = input("User: ")

    run_agent(user_request)