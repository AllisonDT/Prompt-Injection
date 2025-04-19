#!/usr/bin/env python3

import json
import argparse
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, MultipleLocator

def main():
    parser = argparse.ArgumentParser(description="Plot injection success by method and write summary")
    parser.add_argument("input", help="Path to JSON results file")
    args = parser.parse_args()

    # Load data
    with open(args.input, "r") as f:
        data = json.load(f)

    # Define methods and categories
    methods = [
        "Ignore Instructions", "Role Play", "Comment Injection",
        "Chain-of-Thought", "Code Injection", "Jailbreak", "Other"
    ]
    plot_cats = ["Full", "Username-only", "Password-only"]
    all_cats = plot_cats + ["None"]

    # Initialize counts
    counts = {m: {cat: 0 for cat in all_cats} for m in methods}

    # Tally results in one pass
    for item in data:
        m = item.get("method")
        if m not in counts:
            continue
        u = item.get("isUsernameReturned", False)
        p = item.get("isPasswordReturned", False)

        if u and p:
            counts[m]["Full"] += 1
        elif u:
            counts[m]["Username-only"] += 1
        elif p:
            counts[m]["Password-only"] += 1
        else:
            counts[m]["None"] += 1

    # --- Plotting (only Full, Username-only, Password-only) ---
    x = list(range(len(methods)))
    width = 0.25
    offsets = [-width, 0, width]

    fig, ax = plt.subplots()
    for i, cat in enumerate(plot_cats):
        vals = [counts[m][cat] for m in methods]
        ax.bar([xi + offsets[i] for xi in x], vals, width, label=cat)

    ax.set_xticks(x)
    ax.set_xticklabels(methods, rotation=45, ha="right")
    ax.set_ylabel("Number of Successful Injections")
    ax.set_title(f"Injection Success by Method (N = {len(data)})")

    # Major ticks = integers only
    ax.yaxis.get_major_locator().set_params(integer=True)
    # Minor ticks = every integer
    ax.yaxis.set_minor_locator(MultipleLocator(1))

    # Set y‑limit a bit above max
    max_count = max(counts[m][cat] for m in methods for cat in plot_cats)
    buffer = max(1, int(max_count * 0.1))
    ax.set_ylim(0, max_count + buffer)

    ax.legend()
    plt.tight_layout()
    plt.savefig("results/injection_success.png", dpi=300)

    # --- Summary file ---
    overall_total = len(data)
    overall_success = sum(counts[m][cat] for m in methods for cat in plot_cats)
    success_pct = (overall_success / overall_total * 100) if overall_total else 0

    with open("results/summary.txt", "w") as f:
        f.write(f"Overall prompts evaluated: {overall_total}\n")
        f.write(f"Overall success rate: {overall_success}/{overall_total} ({success_pct:.1f}%)\n\n")
        for m in methods:
            m_total = sum(counts[m][cat] for cat in all_cats)
            f.write(f"Method: {m}\n")
            f.write(f"  Total prompts: {m_total}\n")
            for cat in all_cats:
                cnt = counts[m][cat]
                pct = (cnt / m_total * 100) if m_total else 0
                f.write(f"    {cat}: {cnt} ({pct:.1f}%)\n")
            f.write("\n")

if __name__ == "__main__":
    main()