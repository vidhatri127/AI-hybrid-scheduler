"""
output_module.py
----------------
Renders the scheduler results to the console.

Prints:
  1. Selected algorithm
  2. AI decision trace
  3. Gantt chart (text + optional matplotlib visual)
  4. Per-process table (Arrival, Burst, Completion, WT, TAT)
  5. Average WT and average TAT
"""


# ══════════════════════════════════════════════════════════════════════════════
# Public entry point
# ══════════════════════════════════════════════════════════════════════════════

def display(results: dict, decision_trace: str = "", show_visual: bool = True) -> None:
    """
    Print all scheduling results to stdout and optionally show a visual chart.

    Parameters
    ----------
    results       : dict returned by execution_engine.run()
    decision_trace: str  returned by ai_decision.explain_decision()
    show_visual   : bool if True, attempt to render a matplotlib Gantt chart
    """
    _print_header()
    _print_algorithm(results["algorithm"])
    if decision_trace:
        _print_decision_trace(decision_trace)
    _print_gantt_text(results["timeline"])
    _print_metrics_table(results["metrics"])
    _print_averages(results["avg_wt"], results["avg_tat"])

    if show_visual:
        _render_visual_gantt(results["timeline"], results["algorithm"])


# ══════════════════════════════════════════════════════════════════════════════
# Internal helpers
# ══════════════════════════════════════════════════════════════════════════════

def _print_header() -> None:
    print()
    print("=" * 62)
    print("   AI-Driven Hybrid Process Scheduler - Results")
    print("=" * 62)


def _print_algorithm(name: str) -> None:
    print(f"\n  Selected Algorithm : {name}\n")


def _print_decision_trace(trace: str) -> None:
    print("  AI Decision Trace:")
    print(trace)
    print()


def _print_gantt_text(timeline: list) -> None:
    """Print a text-based Gantt chart."""
    print("  Execution Timeline (Gantt Chart):")
    print("  " + str([(pid, s, e) for pid, s, e in timeline]))

    # ASCII bar chart
    print()
    print("  " + "-" * 56)
    bar_line = "  |"
    time_line = "   "
    for (pid, start, end) in timeline:
        width  = (end - start) * 3         # scale: 3 chars per time unit
        cell   = pid.center(max(width, len(pid) + 2))
        bar_line  += cell + "|"
        # Mark the start time below each block
        time_line += str(start).ljust(max(width + 1, len(pid) + 3))

    print(bar_line)
    print("  " + "-" * 56)
    # Append final end time
    last_end = timeline[-1][2]
    time_line = time_line.rstrip() + str(last_end)
    print("  " + time_line.lstrip(" " * 1))
    print()


def _print_metrics_table(metrics: list) -> None:
    """Print the per-process statistics table."""
    header = f"  {'Process':<10} {'Arrival':>7} {'Burst':>6} {'Completion':>11} {'WT':>5} {'TAT':>6}"
    sep    = "  " + "-" * 56
    print(header)
    print(sep)
    for m in metrics:
        print(
            f"  {m['process_id']:<10}"
            f" {m['arrival_time']:>7}"
            f" {m['burst_time']:>6}"
            f" {m['completion_time']:>11}"
            f" {m['waiting_time']:>5}"
            f" {m['turnaround_time']:>6}"
        )
    print(sep)


def _print_averages(avg_wt: float, avg_tat: float) -> None:
    print(f"\n  Avg Waiting Time    : {avg_wt:.2f}")
    print(f"  Avg Turnaround Time : {avg_tat:.2f}")
    print()
    print("=" * 62)
    print()


# ══════════════════════════════════════════════════════════════════════════════
# Optional: matplotlib visual Gantt chart
# ══════════════════════════════════════════════════════════════════════════════

def _render_visual_gantt(timeline: list, algorithm: str) -> None:
    """
    Render a colour-coded horizontal bar (Gantt) chart using matplotlib.
    Silently skips if matplotlib is not installed.
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
    except ImportError:
        print("  [Info] matplotlib not found - skipping visual chart.")
        print("         Install with: pip install matplotlib\n")
        return

    # Collect unique process IDs (preserving timeline order)
    pids_seen = []
    for (pid, _, _) in timeline:
        if pid not in pids_seen:
            pids_seen.append(pid)

    # Assign a distinct colour to each process
    colours = plt.cm.get_cmap("tab10", len(pids_seen))
    colour_map = {pid: colours(i) for i, pid in enumerate(pids_seen)}

    fig, ax = plt.subplots(figsize=(max(10, len(timeline) * 1.2), 3))
    ax.set_title(f"Gantt Chart - {algorithm}", fontsize=14, fontweight="bold", pad=12)

    bar_height = 0.5
    bar_y      = 0.25   # vertical centre

    for (pid, start, end) in timeline:
        width = end - start
        ax.barh(
            bar_y,
            width,
            left=start,
            height=bar_height,
            color=colour_map[pid],
            edgecolor="white",
            linewidth=1.5,
        )
        # Label each block with the process ID
        ax.text(
            start + width / 2,
            bar_y,
            pid,
            ha="center",
            va="center",
            fontsize=9,
            fontweight="bold",
            color="white",
        )

    # Time axis
    all_times = sorted({t for (_, s, e) in timeline for t in (s, e)})
    ax.set_xticks(all_times)
    ax.set_xticklabels([str(t) for t in all_times])
    ax.set_xlim(0, timeline[-1][2])
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel("Time Units", fontsize=10)
    ax.spines[["top", "right", "left"]].set_visible(False)

    # Legend
    legend_patches = [
        mpatches.Patch(color=colour_map[pid], label=pid)
        for pid in pids_seen
    ]
    ax.legend(
        handles=legend_patches,
        loc="upper right",
        framealpha=0.85,
        fontsize=8,
    )

    plt.tight_layout()
    plt.show()
