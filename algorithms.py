"""
algorithms.py
-------------
Implements all four CPU scheduling algorithms.

Every function receives a list of normalised process dicts and returns
an execution timeline — a list of tuples:
    [(process_id, start_time, end_time), ...]

Algorithms implemented
──────────────────────
1. FCFS     – First Come First Served (non-preemptive, arrival order)
2. SJF      – Shortest Job First      (non-preemptive, by burst_time)
3. RR       – Round Robin             (time quantum = 2, arrival-aware)
4. Priority – Priority Scheduling     (non-preemptive, lower number = higher)
"""

import copy


# ══════════════════════════════════════════════════════════════════════════════
# 1. FCFS — First Come First Served
# ══════════════════════════════════════════════════════════════════════════════

def fcfs(processes: list) -> list:
    """
    Schedule processes in arrival order (non-preemptive).
    Ties in arrival_time are broken by process_id (alphabetical).
    """
    # Processes are already sorted by arrival_time from input_handler
    timeline = []
    current_time = 0

    for proc in processes:
        # CPU idles if no process has arrived yet
        start = max(current_time, proc["arrival_time"])
        end   = start + proc["burst_time"]
        timeline.append((proc["process_id"], start, end))
        current_time = end

    return timeline


# ══════════════════════════════════════════════════════════════════════════════
# 2. SJF — Shortest Job First (non-preemptive)
# ══════════════════════════════════════════════════════════════════════════════

def sjf(processes: list) -> list:
    """
    At each scheduling decision point, pick the arrived process with
    the shortest burst_time. Ties broken by arrival_time then process_id.
    """
    remaining = copy.deepcopy(processes)   # work on a copy
    timeline   = []
    current_time = 0

    while remaining:
        # Collect all processes that have arrived by current_time
        available = [p for p in remaining if p["arrival_time"] <= current_time]

        if not available:
            # CPU idle — jump to the next earliest arrival
            current_time = min(p["arrival_time"] for p in remaining)
            continue

        # Pick shortest burst; tie-break by arrival_time, then process_id
        chosen = min(
            available,
            key=lambda p: (p["burst_time"], p["arrival_time"], p["process_id"])
        )

        start = current_time
        end   = start + chosen["burst_time"]
        timeline.append((chosen["process_id"], start, end))
        current_time = end
        remaining.remove(chosen)

    return timeline


# ══════════════════════════════════════════════════════════════════════════════
# 3. Round Robin (time quantum = 2)
# ══════════════════════════════════════════════════════════════════════════════

def round_robin(processes: list, quantum: int = 2) -> list:
    """
    Round Robin with a configurable time quantum (default = 2).

    Arrival-aware queue: a process enters the ready queue only when
    current_time >= its arrival_time.  After each quantum the process is
    re-enqueued at the back; newly arrived processes are added first so
    that the scheduler always sees fresh arrivals before the preempted tail.
    """
    # Build working copies with remaining burst time
    remaining = [
        {**copy.deepcopy(p), "remaining": p["burst_time"]}
        for p in processes
    ]
    # Sort by arrival first so we can efficiently find new arrivals
    remaining.sort(key=lambda p: (p["arrival_time"], p["process_id"]))

    timeline     = []
    current_time = 0
    ready_queue  = []      # list of process dicts in FIFO order
    enqueued_ids = set()   # track which PIDs are already in the queue

    # Helper: enqueue all processes that have arrived by `current_time`
    def enqueue_arrivals():
        for proc in remaining:
            if (proc["arrival_time"] <= current_time
                    and proc["process_id"] not in enqueued_ids
                    and proc["remaining"] > 0):
                ready_queue.append(proc)
                enqueued_ids.add(proc["process_id"])

    enqueue_arrivals()

    while ready_queue or any(p["remaining"] > 0 for p in remaining):
        if not ready_queue:
            # CPU idle — advance to next process arrival
            next_arrival = min(
                p["arrival_time"]
                for p in remaining if p["remaining"] > 0
            )
            current_time = next_arrival
            enqueue_arrivals()
            continue

        proc = ready_queue.pop(0)

        # Execute for min(quantum, remaining burst)
        run_time = min(quantum, proc["remaining"])
        start    = current_time
        end      = start + run_time
        timeline.append((proc["process_id"], start, end))

        current_time      = end
        proc["remaining"] -= run_time

        # Enqueue newly arrived processes BEFORE re-queuing the current one
        enqueue_arrivals()

        if proc["remaining"] > 0:
            ready_queue.append(proc)   # re-queue at the back

    return timeline


# ══════════════════════════════════════════════════════════════════════════════
# 4. Priority Scheduling (non-preemptive)
# ══════════════════════════════════════════════════════════════════════════════

def priority_scheduling(processes: list) -> list:
    """
    Non-preemptive priority scheduling.
    Lower priority number = higher priority.
    Ties broken by arrival_time then process_id.
    """
    remaining = copy.deepcopy(processes)
    timeline   = []
    current_time = 0

    while remaining:
        # Collect processes that have arrived
        available = [p for p in remaining if p["arrival_time"] <= current_time]

        if not available:
            # CPU idle
            current_time = min(p["arrival_time"] for p in remaining)
            continue

        # Pick highest priority (lowest number); tie-break by arrival then pid
        chosen = min(
            available,
            key=lambda p: (
                p["priority"] if p["priority"] is not None else float("inf"),
                p["arrival_time"],
                p["process_id"],
            )
        )

        start = current_time
        end   = start + chosen["burst_time"]
        timeline.append((chosen["process_id"], start, end))
        current_time = end
        remaining.remove(chosen)

    return timeline
