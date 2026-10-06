"""Day 4: Estimate memory needed by local open LLMs."""

# Bytes per parameter from the Day 4 lab
BYTES_PER_PARAM = {
    "FP16": 2.00,
    "Q8_0": 1.00,
    "Q6_K": 0.81,
    "Q5_K_M": 0.68,
    "Q4_K_M": 0.57,
    "Q3_K_M": 0.43,
}

# KV-cache estimate from the Day 4 lab
KV_GB_PER_B_PER_1K = 0.02

# Runtime overhead
OVERHEAD = 1.10


def estimate(params_b, precision="Q4_K_M", context_k=8):
    """Calculate weights, KV cache and total memory."""

    if precision not in BYTES_PER_PARAM:
        raise ValueError(
            f"Unknown precision {precision}. "
            f"Choose from {list(BYTES_PER_PARAM)}"
        )

    weights_gb = params_b * BYTES_PER_PARAM[precision]

    kv_gb = params_b * context_k * KV_GB_PER_B_PER_1K

    total_gb = (weights_gb + kv_gb) * OVERHEAD

    return weights_gb, kv_gb, total_gb


def verdict(total_gb, available_gb):
    """Check whether the estimated memory fits."""

    if total_gb <= available_gb * 0.7:
        return "fits comfortably"

    if total_gb <= available_gb:
        return "fits, but tight"

    return "does NOT fit"


def report(name, params_b, precision, context_k, available_gb):
    """Print one model's memory estimate."""

    weights, kv, total = estimate(
        params_b,
        precision,
        context_k
    )

    print(
        f"{name:<22} "
        f"{precision:<8} "
        f"{params_b:>5.1f}B "
        f"ctx {context_k:>3}K "
        f"weights {weights:>6.2f} GB "
        f"KV {kv:>5.2f} GB "
        f"total {total:>6.2f} GB "
        f"-> {verdict(total, available_gb)}"
    )


if __name__ == "__main__":

    # Your available system RAM
    AVAILABLE_GB = 16.0

    print(f"Memory available: {AVAILABLE_GB} GB\n")

    # --------------------------------------------------
    # Part 1: Four model configurations
    # --------------------------------------------------

    print("MODEL ESTIMATES")
    print("-" * 100)

    report(
        "Qwen3 4B",
        4.0,
        "Q4_K_M",
        4,
        AVAILABLE_GB
    )

    report(
        "Qwen3 4B",
        4.0,
        "Q4_K_M",
        8,
        AVAILABLE_GB
    )

    report(
        "Qwen3 8B",
        8.0,
        "Q4_K_M",
        8,
        AVAILABLE_GB
    )

    report(
        "Qwen3 8B",
        8.0,
        "Q8_0",
        8,
        AVAILABLE_GB
    )

    # --------------------------------------------------
    # Part 2: Context-length experiment
    # --------------------------------------------------

    print("\nCONTEXT LENGTH EXPERIMENT")
    print("-" * 100)

    for context_k in (4, 8, 16, 32):

        report(
            "Qwen3 4B",
            4.0,
            "Q4_K_M",
            context_k,
            AVAILABLE_GB
        )

    # --------------------------------------------------
    # Part 3: Quantization experiment
    # --------------------------------------------------

    print("\nQUANTIZATION EXPERIMENT")
    print("-" * 100)

    for precision in (
        "Q3_K_M",
        "Q4_K_M",
        "Q5_K_M",
        "Q6_K",
        "Q8_0",
        "FP16"
    ):

        report(
            "Qwen3 4B",
            4.0,
            precision,
            8,
            AVAILABLE_GB
        )