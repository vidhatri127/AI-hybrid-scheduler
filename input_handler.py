"""
input_handler.py
----------------
Parses and validates the raw list of process dictionaries.
Ensures required fields exist, types are correct, and applies
default values (priority=None) for optional fields.
"""


def validate_and_normalize(processes: list) -> list:
    """
    Validate and normalise a list of raw process dictionaries.

    Each dict must contain:
        - process_id  : str   — unique identifier (e.g. 'P1')
        - arrival_time: int   — time unit when the process arrives (>= 0)
        - burst_time  : int   — CPU time needed (> 0)
        - priority    : int | None  — optional; lower = higher priority

    Returns a sorted (by arrival_time) list of clean process dicts.
    Raises ValueError for any invalid or missing fields.
    """
    if not processes:
        raise ValueError("Process list is empty. Provide at least one process.")

    required_fields = {"process_id", "arrival_time", "burst_time"}
    seen_ids = set()
    normalized = []

    for idx, proc in enumerate(processes):
        # ── Check required fields ──────────────────────────────────────────
        missing = required_fields - proc.keys()
        if missing:
            raise ValueError(
                f"Process at index {idx} is missing required fields: {missing}"
            )

        pid = proc["process_id"]
        arrival = proc["arrival_time"]
        burst = proc["burst_time"]
        priority = proc.get("priority", None)   # optional; default = None

        # ── Type checks ────────────────────────────────────────────────────
        if not isinstance(pid, str) or not pid.strip():
            raise TypeError(f"process_id must be a non-empty string (index {idx}).")

        if not isinstance(arrival, int) or arrival < 0:
            raise ValueError(
                f"arrival_time must be a non-negative integer for '{pid}'."
            )

        if not isinstance(burst, int) or burst <= 0:
            raise ValueError(
                f"burst_time must be a positive integer for '{pid}'."
            )

        if priority is not None:
            if not isinstance(priority, int):
                raise TypeError(f"priority must be an integer or None for '{pid}'.")

        # ── Uniqueness check ───────────────────────────────────────────────
        if pid in seen_ids:
            raise ValueError(f"Duplicate process_id detected: '{pid}'.")
        seen_ids.add(pid)

        normalized.append({
            "process_id":   pid.strip(),
            "arrival_time": arrival,
            "burst_time":   burst,
            "priority":     priority,
        })

    # Sort by arrival time (ties broken by original order / process_id)
    normalized.sort(key=lambda p: (p["arrival_time"], p["process_id"]))
    return normalized
