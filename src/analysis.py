#!/usr/bin/env python3
"""
analysis.py

2-D sweep over λ_b and λ_a, save CSV of (λ_b, λ_a, clearing_fraction),
and write out a plot with one curve per λ_b, all inside a timestamped data folder.

Usage:
    python src/analysis.py \
      -b 4 8 16 \
      -a 5 10 20 40 80 160 \
      -n 200000 \
      --logx
"""

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import argparse
from datetime import datetime
from simulation import simulate

def sweep_2d(lambda_bs, lambda_as, num_voxels):
    """Return list of (b, a, clearing_fraction) tuples."""
    results = []
    for lb in lambda_bs:
        for la in lambda_as:
            frac = simulate(lb, la, num_voxels)
            results.append((lb, la, frac))
    return results

def main():
    parser = argparse.ArgumentParser(
        description="2D sweep over λ_b and λ_a, save results in timestamped folder"
    )
    parser.add_argument(
        "--lambda-b", "-b",
        type=float, nargs="+", required=True,
        help="Space-delimited list of base means λ_b"
    )
    parser.add_argument(
        "--lambda-a", "-a",
        type=float, nargs="+", required=True,
        help="Space-delimited list of acid means λ_a"
    )
    parser.add_argument(
        "--num-voxels", "-n",
        type=int, default=1_000_000,
        help="Number of voxels per simulation"
    )
    parser.add_argument(
        "--logx",
        action="store_true",
        help="Log scale on x axis (λ_a)"
    )
    args = parser.parse_args()

    # Build a timestamped output directory under data/
    # __file__ is src/analysis.py, so go up one level and into data/
    base_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = os.path.join(base_data_dir, timestamp)
    os.makedirs(out_dir, exist_ok=True)

    # Default filenames inside that folder
    csv_filename  = "multi_sweep_results.csv"
    plot_filename = "multi_clearing_vs_lambda.png"
    csv_path  = os.path.join(out_dir, csv_filename)
    plot_path = os.path.join(out_dir, plot_filename)

    # Run the 2D sweep
    data = sweep_2d(args.lambda_b, args.lambda_a, args.num_voxels)

    # Write CSV
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["lambda_b", "lambda_a", "clearing_fraction"])
        writer.writerows(data)
    print(f"✓ Data saved to {csv_path}")

    # Plot one curve per λ_b
    plt.figure()
    for lb in sorted(set(args.lambda_b)):
        la_vals = [la for (b, la, _) in data if b == lb]
        fracs   = [f  for (b, la, f)  in data if b == lb]
        plt.plot(la_vals, fracs, marker="o", label=f"λ_b={lb}")

    if args.logx:
        plt.xscale("log")
    plt.xlabel("Mean acid per voxel (λ_a)")
    plt.ylabel("Clearing fraction")
    plt.title("Clearing fraction vs λ_a for different λ_b")
    plt.grid(True)
    plt.legend(title="Base means")
    plt.tight_layout()

    # Save and show
    plt.savefig(plot_path)
    print(f"✓ Plot saved to {plot_path}")
    plt.show()

if __name__ == "__main__":
    main()