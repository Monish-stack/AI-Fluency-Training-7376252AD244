from main import run_tool


tests = [
    ("get_class", '{"day":"Monday"}'),

    # 1. Missing argument
    ("get_class", '{}'),

    # 2. Extra argument
    ("get_class", '{"day":"Monday","name":"Monish"}'),

    # 3. Wrong type
    ("get_class", '{"day":123}'),

    # 4. Invalid enum value
    ("get_class", '{"day":"Sunday"}'),

    # 5. Unknown tool
    ("get_marks", '{"day":"Monday"}'),

    # 6. Invalid JSON
    ("get_class", '{"day":"Monday"'),

    # 7. Null value
    ("get_room", '{"day":null}'),

    # 8. Extra designed fault
    ("get_room", '{"day":"Monday","room":"A-101"}')
]


print("=" * 50)
print("FAULT INJECTION TEST")
print("=" * 50)

for number, (tool, raw_args) in enumerate(tests, 1):

    print("\nTest", number)
    print("Tool:", tool)
    print("Arguments:", raw_args)

    if tool not in ["get_class", "get_room"]:
        print("Result: Unknown tool.")
        continue

    try:
        import json
        args = json.loads(raw_args)
    except json.JSONDecodeError:
        print("Result: Invalid JSON arguments.")
        continue

    result = run_tool(tool, args)

    print("Result:", result)