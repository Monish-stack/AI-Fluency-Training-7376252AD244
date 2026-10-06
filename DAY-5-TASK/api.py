import requests
import time


# ============================================================
# CONFIGURATION
# ============================================================

OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "college-study-assistant"

GENERATE_URL = f"{OLLAMA_URL}/api/generate"
OPENAI_URL = f"{OLLAMA_URL}/v1/chat/completions"


# ============================================================
# HELPER FUNCTION
# ============================================================

def print_separator():
    print("\n" + "=" * 70 + "\n")


# ============================================================
# 1. NON-STREAMING REQUEST
#    Ollama REST API: /api/generate
# ============================================================

def non_streaming_test(prompt):
    print_separator()
    print("1. NON-STREAMING TEST")
    print("Endpoint: /api/generate")
    print(f"Prompt: {prompt}\n")

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    start_time = time.perf_counter()

    response = requests.post(
        GENERATE_URL,
        json=payload
    )

    end_time = time.perf_counter()

    if response.status_code != 200:
        print("Error:", response.status_code)
        print(response.text)
        return

    data = response.json()

    total_time = end_time - start_time

    print("MODEL RESPONSE:")
    print(data.get("response", ""))

    print("\n--- PERFORMANCE ---")

    # Ollama reports these values in nanoseconds.
    total_duration = data.get("total_duration", 0) / 1_000_000_000

    load_duration = data.get("load_duration", 0) / 1_000_000_000

    eval_count = data.get("eval_count", 0)

    eval_duration = data.get("eval_duration", 0) / 1_000_000_000

    if eval_duration > 0:
        tokens_per_second = eval_count / eval_duration
    else:
        tokens_per_second = 0

    print(f"Total time measured by Python : {total_time:.2f} seconds")
    print(f"Total duration from Ollama    : {total_duration:.2f} seconds")
    print(f"Model load time               : {load_duration:.2f} seconds")
    print(f"Generated tokens              : {eval_count}")
    print(f"Tokens per second             : {tokens_per_second:.2f}")


# ============================================================
# 2. STREAMING REQUEST
#    Ollama REST API: /api/generate
# ============================================================

def streaming_test(prompt):
    print_separator()
    print("2. STREAMING TEST")
    print("Endpoint: /api/generate")
    print(f"Prompt: {prompt}\n")

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True
    }

    start_time = time.perf_counter()
    first_token_time = None

    total_tokens = 0
    full_response = ""

    print("MODEL RESPONSE:")
    print()

    response = requests.post(
        GENERATE_URL,
        json=payload,
        stream=True
    )

    if response.status_code != 200:
        print("Error:", response.status_code)
        print(response.text)
        return

    for line in response.iter_lines():

        if not line:
            continue

        data = line.decode("utf-8")

        try:
            import json
            chunk = json.loads(data)
        except json.JSONDecodeError:
            continue

        token = chunk.get("response", "")

        if token:

            # Record the time when the first token arrives.
            if first_token_time is None:
                first_token_time = time.perf_counter()

            print(token, end="", flush=True)

            full_response += token
            total_tokens += 1

    end_time = time.perf_counter()

    print("\n")

    total_time = end_time - start_time

    if first_token_time is not None:
        ttft = first_token_time - start_time
    else:
        ttft = 0

    if total_time > 0:
        tokens_per_second = total_tokens / total_time
    else:
        tokens_per_second = 0

    print("--- PERFORMANCE ---")
    print(f"TTFT                  : {ttft:.2f} seconds")
    print(f"Total time            : {total_time:.2f} seconds")
    print(f"Generated tokens      : {total_tokens}")
    print(f"Tokens per second     : {tokens_per_second:.2f}")

    print("\nNote:")
    print("TTFT measures how long it took before the first output appeared.")
    print("Total time measures the complete request duration.")


# ============================================================
# 3. OPENAI-COMPATIBLE ENDPOINT
# ============================================================

def openai_compatible_test(prompt):
    print_separator()
    print("3. OPENAI-COMPATIBLE ENDPOINT TEST")
    print("Endpoint: /v1/chat/completions")
    print(f"Prompt: {prompt}\n")

    # IMPORTANT:
    # This system prompt is intentionally different from
    # the SYSTEM instruction in the Modelfile.
    #
    # Modelfile system prompt:
    # "You are a college study assistant..."
    #
    # Program system prompt:
    # "You are a strict exam evaluator..."
    #
    # This demonstrates that the application can provide
    # its own system instruction.

    messages = [
        {
            "role": "system",
            "content": (
                "You are a strict exam evaluator. "
                "Answer in exactly 2 short sentences. "
                "Do not give motivational advice."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False
    }

    start_time = time.perf_counter()

    response = requests.post(
        OPENAI_URL,
        json=payload
    )

    end_time = time.perf_counter()

    if response.status_code != 200:
        print("Error:", response.status_code)
        print(response.text)
        return

    data = response.json()

    total_time = end_time - start_time

    print("MODEL RESPONSE:")

    try:
        answer = data["choices"][0]["message"]["content"]
        print(answer)
    except (KeyError, IndexError):
        print(data)

    print(f"\nTotal time: {total_time:.2f} seconds")


# ============================================================
# 4. CHECK MODEL STATUS
#    Uses Ollama /api/ps
# ============================================================

def check_model_status():
    print_separator()
    print("4. CHECKING LOADED MODELS")
    print("Endpoint: /api/ps\n")

    try:
        response = requests.get(
            f"{OLLAMA_URL}/api/ps"
        )

        if response.status_code != 200:
            print("Could not retrieve model status.")
            return

        data = response.json()

        models = data.get("models", [])

        if not models:
            print("No model is currently loaded.")
            return

        print("Currently loaded models:")

        for model in models:
            print(
                f"- {model.get('name', 'Unknown')} "
                f"| Size: {model.get('size', 'Unknown')}"
            )

    except requests.exceptions.ConnectionError:
        print("Could not connect to Ollama.")


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("=" * 70)
    print("COLLEGE STUDY ASSISTANT - OLLAMA REST API DEMO")
    print("=" * 70)

    print("\nMake sure Ollama is running.")
    print(f"Using model: {MODEL_NAME}")

    # --------------------------------------------------------
    # Check whether model is loaded
    # --------------------------------------------------------

    check_model_status()

    # --------------------------------------------------------
    # Prompt 1
    # --------------------------------------------------------

    prompt1 = (
        "Explain what an array is in Java "
        "for a beginner."
    )

    non_streaming_test(prompt1)

    # --------------------------------------------------------
    # Prompt 2
    # --------------------------------------------------------

    prompt2 = (
        "Explain the difference between "
        "stack and queue in simple terms."
    )

    streaming_test(prompt2)

    # --------------------------------------------------------
    # Prompt 3
    # --------------------------------------------------------

    prompt3 = (
        "I have an exam tomorrow and I am confused "
        "about binary search. Explain it."
    )

    openai_compatible_test(prompt3)

    # --------------------------------------------------------
    # Check model again
    # --------------------------------------------------------

    check_model_status()

    print_separator()
    print("DEMO COMPLETED")


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
