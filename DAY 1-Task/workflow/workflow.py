import json
from datetime import datetime


def load_student_data():
    with open("../data/student_data.json", "r") as file:
        return json.load(file)


def find_highest_fee_course(courses):
    highest_course = courses[0]

    for course in courses:
        if course["fee"] > highest_course["fee"]:
            highest_course = course

    return highest_course


def should_prioritize(course):
    today = datetime.now().date()
    deadline = datetime.strptime(course["deadline"], "%Y-%m-%d").date()

    if course["status"] == "Pending" and deadline >= today:
        return True

    return False


def run_workflow():
    print("\n===== RULE-BASED WORKFLOW =====\n")

    # Step 1: Load private data
    data = load_student_data()

    # Step 2: Get course information
    courses = data["courses"]

    # Step 3: Find the course with the highest fee
    highest_course = find_highest_fee_course(courses)

    # Step 4: Apply predefined rule
    priority = should_prioritize(highest_course)

    # Step 5: Generate result
    print("Student:", data["student"]["name"])
    print("Registration Number:", data["student"]["registration_number"])

    print("\nHighest Fee Course:")
    print("Course:", highest_course["name"])
    print("Fee: ₹", highest_course["fee"])
    print("Deadline:", highest_course["deadline"])
    print("Status:", highest_course["status"])

    if priority:
        print("\nRecommendation: Prioritize paying this course.")
    else:
        print("\nRecommendation: No immediate payment priority.")


if __name__ == "__main__":
    run_workflow()