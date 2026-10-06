from openai import OpenAI
import json

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

MODEL = "college-study-assistant"

# -----------------------------
# DATA
# -----------------------------

timetable = {
    "Monday": {"class": "Data Structures", "room": "A-101"},
    "Tuesday": {"class": "DBMS", "room": "B-202"},
    "Wednesday": {"class": "Java", "room": "A-102"},
    "Thursday": {"class": "Computer Networks", "room": "B-201"},
    "Friday": {"class": "AI", "room": "A-103"}
}


# -----------------------------
# TOOLS
# -----------------------------

def get_class(day):
    return timetable[day]["class"]


def get_room(day):
    return timetable[day]["room"]


# -----------------------------
# SCHEMAS
# -----------------------------

SCHEMAS = {
    "get_class": {
        "type": "function",
        "function": {
            "name": "get_class",
            "description": "Get the class for a particular day.",
            "parameters": {
                "type": "object",
                "properties": {
                    "day": {
                        "type": "string",
                        "enum": [
                            "Monday",
                            "Tuesday",
                            "Wednesday",
                            "Thursday",
                            "Friday"
                        ]
                    }
                },
                "required": ["day"],
                "additionalProperties": False
            }
        }
    },

    "get_room": {
        "type": "function",
        "function": {
            "name": "get_room",
            "description": "Get the room for a particular day.",
            "parameters": {
                "type": "object",
                "properties": {
                    "day": {
                        "type": "string",
                        "enum": [
                            "Monday",
                            "Tuesday",
                            "Wednesday",
                            "Thursday",
                            "Friday"
                        ]
                    }
                },
                "required": ["day"],
                "additionalProperties": False
            }
        }
    }
}


# -----------------------------
# VALIDATION
# -----------------------------

def validate(name, args):

    if name not in SCHEMAS:
        return "Unknown tool."

    schema = SCHEMAS[name]["function"]["parameters"]

    if "day" not in args:
        return "Missing required argument: day."

    if len(args) > 1:
        return "Extra argument found. Only day is allowed."

    if not isinstance(args["day"], str):
        return "Wrong type. day must be a string."

    if args["day"] not in schema["properties"]["day"]["enum"]:
        return "Invalid day. Use Monday to Friday."

    return None


# -----------------------------
# RUN TOOL
# -----------------------------

def run_tool(name, args):

    error = validate(name, args)

    if error:
        return error

    if name == "get_class":
        return get_class(args["day"])

    if name == "get_room":
        return get_room(args["day"])

    return "Unknown tool."


# -----------------------------
# AGENT
# -----------------------------

def ask(question):

    messages = [
        {
            "role": "system",
            "content": (
                "You are a college timetable assistant. "
                "Use the available tools when timetable information "
                "is needed. Do not invent timetable information."
            )
        },
        {
            "role": "user",
            "content": question
        }
    ]

    tools = list(SCHEMAS.values())

    for step in range(5):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=300
        )

        choice = response.choices[0]

        print("\nStep:", step + 1)
        print("Finish reason:", choice.finish_reason)

        if choice.finish_reason == "length":
            print("Response was too long.")
            continue

        message = choice.message

        if not message.tool_calls:
            print("\nAnswer:")
            print(message.content)
            return

        messages.append(message)

        for call in message.tool_calls:

            name = call.function.name
            raw_args = call.function.arguments

            print("Tool:", name)
            print("Arguments:", raw_args)

            try:
                args = json.loads(raw_args)
            except json.JSONDecodeError:
                result = "Invalid JSON arguments."

                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result
                })

                continue

            result = run_tool(name, args)

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result)
            })


# -----------------------------
# MAIN
# -----------------------------

print("=" * 50)
print("COLLEGE TIMETABLE ASSISTANT")
print("=" * 50)

ask("What class do I have on Monday?")

ask("What class and room do I have on Wednesday?")

ask("What is my class on Sunday?")

ask("Explain what a timetable is.")