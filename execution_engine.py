"""
execution_engine.py
-------------------
Orchestrates the full scheduling run.

Responsibilities:
  1. Call the correct algorithm function from algorithms.py
  2. Compute per-process metrics from the returned timeline:
       completion_time = end time of the process's last segment
       TAT             = completion_time - arrival_time
       WT              = TAT - burst_time
  3. Return a structured results dict containing the timeline and metrics.
"""

from algorithms import fcfs, sjf, round_robin, priority_scheduling


# Map algorithm names (returned by ai_decision) to callable functions
_ALGORITHM_MAP = {
    "FCFS":        fcfs,
    "SJF":         sjf,
    "Round Robin": round_robin,
    "Priority":    priority_scheduling,
}


def run(processes: list, algorithm: str) -> dict:
    """
    Execute the chosen algorithm and compute per-process statistics.

    Parameters
    ----------
    processes : list of normalised process dicts
    algorithm : str — one of 'FCFS', 'SJF', 'Round Robin', 'Priority'

    Returns
    -------
    dict with keys:
        'algorithm'  : str          — algorithm name used
        'timeline'   : list         — [(pid, start, end), ...]
        'metrics'    : list of dict — per-process stats
        'avg_wt'     : float        — average waiting time
        'avg_tat'    : float        — average turnaround time
    """
    if algorithm not in _ALGORITHM_MAP:
        raise ValueError(
            f"Unknown algorithm '{algorithm}'. "
            f"Valid options: {list(_ALGORITHM_MAP.keys())}"
        )

    # ── Step 1: Run the selected scheduling algorithm ──────────────────────
    algo_fn  = _ALGORITHM_MAP[algorithm]
    timeline = algo_fn(processes)

    # ── Step 2: Compute completion times from the timeline ─────────────────
    # A process may appear multiple times in RR — take the last end_time.
    completion_times = {}
    for (pid, start, end) in timeline:
        completion_times[pid] = end   # overwrite keeps the latest

    # ── Step 3: Compute per-process WT and TAT ────────────────────────────
    metrics = []
    for proc in processes:
        pid     = proc["process_id"]
        arrival = proc["arrival_time"]
        burst   = proc["burst_time"]

        ct  = completion_times[pid]
        tat = ct - arrival          # Turnaround Time
        wt  = tat - burst           # Waiting Time

        metrics.append({
            "process_id":       pid,
            "arrival_time":     arrival,
            "burst_time":       burst,
            "completion_time":  ct,
            "waiting_time":     wt,
            "turnaround_time":  tat,
        })

    # ── Step 4: Compute averages ───────────────────────────────────────────
    n       = len(metrics)
    avg_wt  = sum(m["waiting_time"]    for m in metrics) / n
    avg_tat = sum(m["turnaround_time"] for m in metrics) / n

    return {
        "algorithm": algorithm,
        "timeline":  timeline,
        "metrics":   metrics,
        "avg_wt":    avg_wt,
        "avg_tat":   avg_tat,
    }
