import json
from pathlib import Path


# Location of our private student data
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "student_data.json"


def load_data():
    """Load private student data from JSON."""
    with open(DATA_FILE, "r") as file:
        return json.load(file)


def get_student_information():
    """Get private information about the student."""
    data = load_data()

    return {
        "name": data["student"]["name"],
        "registration_number": data["student"]["registration_number"],
        "email": data["student"]["email"]
    }


def get_courses():
    """Get all courses from the private student data."""
    data = load_data()

    return data["courses"]


def get_course_by_name(course_name):
    """Find a specific course by name."""
    data = load_data()

    for course in data["courses"]:
        if course["name"].lower() == course_name.lower():
            return course

    return {
        "error": "Course not found"
    }


def execute_tool(tool_name, arguments):
    """Execute the tool selected by the AI agent."""

    if tool_name == "get_student_information":
        return get_student_information()

    elif tool_name == "get_courses":
        return get_courses()

    elif tool_name == "get_course_by_name":
        return get_course_by_name(
            arguments.get("course_name", "")
        )

    else:
        return {
            "error": f"Unknown tool: {tool_name}"
        }