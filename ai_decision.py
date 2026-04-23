"""
ai_decision.py
--------------
Rule-based AI decision engine.

Evaluates the normalised process list against four ordered rules and
returns the name of the most appropriate scheduling algorithm.

Decision rules (evaluated in strict order):
  Rule 1 → Any process has priority set (not None) → Priority Scheduling
  Rule 2 → Total process count > 7                 → Round Robin  (q=2)
  Rule 3 → Average burst_time < 5                  → SJF
  Rule 4 → Everything else                         → FCFS
"""


def select_algorithm(processes: list) -> str:
    """
    Apply AI decision rules in order and return the chosen algorithm name.

    Parameters
    ----------
    processes : list of normalised process dicts (from input_handler)

    Returns
    -------
    str — one of: 'Priority', 'Round Robin', 'SJF', 'FCFS'
    """
    if not processes:
        raise ValueError("Cannot select an algorithm for an empty process list.")

    # ── Rule 1: Any process has a priority value set ───────────────────────
    if any(p["priority"] is not None for p in processes):
        return "Priority"

    # ── Rule 2: More than 7 processes → Round Robin ────────────────────────
    if len(processes) > 7:
        return "Round Robin"

    # ── Rule 3: Average burst time < 5 → SJF ──────────────────────────────
    avg_burst = sum(p["burst_time"] for p in processes) / len(processes)
    if avg_burst < 5:
        return "SJF"

    # ── Rule 4: Default → FCFS ─────────────────────────────────────────────
    return "FCFS"


def explain_decision(processes: list) -> str:
    """
    Return a human-readable trace of the decision rules that were evaluated.
    Useful for debugging and educational output.
    """
    lines = []
    n = len(processes)

    # Rule 1
    has_priority = any(p["priority"] is not None for p in processes)
    lines.append(
        f"  Rule 1 | Any priority set?         {'YES -> Priority Scheduling selected.' if has_priority else 'NO  -> continue'}"
    )
    if has_priority:
        return "\n".join(lines)

    # Rule 2
    lines.append(
        f"  Rule 2 | Process count ({n}) > 7?  {'YES -> Round Robin selected.' if n > 7 else 'NO  -> continue'}"
    )
    if n > 7:
        return "\n".join(lines)

    # Rule 3
    avg_burst = sum(p["burst_time"] for p in processes) / n
    lines.append(
        f"  Rule 3 | Avg burst ({avg_burst:.2f}) < 5?    {'YES -> SJF selected.' if avg_burst < 5 else 'NO  -> continue'}"
    )
    if avg_burst < 5:
        return "\n".join(lines)

    # Rule 4
    lines.append("  Rule 4 | Default case              -> FCFS selected.")
    return "\n".join(lines)
