"""
main.py
-------
Entry point for the AI-Driven Hybrid Process Scheduler.

HOW TO RUN:
    python main.py

HOW TO MODIFY:
    Edit the `processes` list below with your own process data.
    Each dict supports:
        process_id  : str  (required)
        arrival_time: int  (required, >= 0)
        burst_time  : int  (required, > 0)
        priority    : int  (optional — omit or set to None; lower = higher priority)

Four example scenarios are bundled — uncomment whichever you want to test.
"""

from input_handler   import validate_and_normalize
from ai_decision     import select_algorithm, explain_decision
from execution_engine import run
from output_module   import display


# ══════════════════════════════════════════════════════════════════════════════
# SAMPLE PROCESS LISTS
# ══════════════════════════════════════════════════════════════════════════════

# ── Scenario A: From the PRD — triggers SJF (avg burst = 2.67 < 5) ──────────
processes_sjf = [
    {"process_id": "P1", "arrival_time": 0, "burst_time": 4},
    {"process_id": "P2", "arrival_time": 1, "burst_time": 3},
    {"process_id": "P3", "arrival_time": 2, "burst_time": 1},
]

# ── Scenario B: Priority set → triggers Priority Scheduling ─────────────────
processes_priority = [
    {"process_id": "P1", "arrival_time": 0, "burst_time": 6, "priority": 3},
    {"process_id": "P2", "arrival_time": 1, "burst_time": 4, "priority": 1},
    {"process_id": "P3", "arrival_time": 2, "burst_time": 3, "priority": 2},
]

# ── Scenario C: 8 processes → triggers Round Robin (count > 7) ──────────────
processes_rr = [
    {"process_id": "P1", "arrival_time": 0,  "burst_time": 5},
    {"process_id": "P2", "arrival_time": 1,  "burst_time": 4},
    {"process_id": "P3", "arrival_time": 2,  "burst_time": 3},
    {"process_id": "P4", "arrival_time": 3,  "burst_time": 6},
    {"process_id": "P5", "arrival_time": 4,  "burst_time": 2},
    {"process_id": "P6", "arrival_time": 5,  "burst_time": 7},
    {"process_id": "P7", "arrival_time": 6,  "burst_time": 4},
    {"process_id": "P8", "arrival_time": 7,  "burst_time": 3},
]

# ── Scenario D: Large burst times, ≤ 7 processes → triggers FCFS ────────────
processes_fcfs = [
    {"process_id": "P1", "arrival_time": 0, "burst_time": 10},
    {"process_id": "P2", "arrival_time": 2, "burst_time": 8},
    {"process_id": "P3", "arrival_time": 4, "burst_time": 6},
]


# ══════════════════════════════════════════════════════════════════════════════
# SELECT ACTIVE SCENARIO  ← change this variable to switch examples
# ══════════════════════════════════════════════════════════════════════════════
ACTIVE_PROCESSES = processes_sjf   # ← swap to processes_priority, _rr, _fcfs


# ══════════════════════════════════════════════════════════════════════════════
# MAIN PIPELINE
# ══════════════════════════════════════════════════════════════════════════════

def main():
    # 1. Validate & normalise input
    processes = validate_and_normalize(ACTIVE_PROCESSES)

    # 2. AI decision — pick the best algorithm
    algorithm = select_algorithm(processes)
    trace     = explain_decision(processes)

    # 3. Execute the chosen algorithm & compute metrics
    results = run(processes, algorithm)

    # 4. Display results
    #    Set show_visual=False to skip the matplotlib chart (text-only mode)
    display(results, decision_trace=trace, show_visual=True)


if __name__ == "__main__":
    main()
