# src/analysis_sweep3d.py

#!/usr/bin/env python3
"""
analysis_sweep3d.py

Filter sweep3d_results.csv for a fixed mean depth and compare RMS roughness.
"""

import pandas as pd
import matplotlib.pyplot as plt
import argparse

def main():
    parser = argparse.ArgumentParser(description="Analyze sweep3d results at fixed depth")
    parser.add_argument(
        "--csv", "-i",
        default="data/3d/sweep3d_results.csv",
        help="Path to sweep3d CSV"
    )
    parser.add_argument(
        "--depth", "-d",
        type=float, default=50.0,
        help="Target mean height (layers)"
    )
    parser.add_argument(
        "--tol", "-t",
        type=float, default=1.0,
        help="Tolerance around target depth"
    )
    args = parser.parse_args()

    df = pd.read_csv(args.csv)
    sel = df[(df.mean_h >= args.depth - args.tol) & (df.mean_h <= args.depth + args.tol)]

    if sel.empty:
        print("No runs within ±{:.1f} layers of depth {}".format(args.tol, args.depth))
        return

    # Pivot roughness as function of λ_b for each λ_a0
    pivot = sel.pivot(index="lambda_b", columns="lambda_a0", values="rms_h")

    pivot.plot(marker="o")
    plt.xscale("log"); plt.yscale("log")
    plt.xlabel("Base mean λ_b"); plt.ylabel("RMS roughness σ")
    plt.title(f"RMS roughness at ⟨H⟩≈{args.depth}±{args.tol} layers")
    plt.grid(True, which="both", ls="--", lw=0.5)
    plt.legend(title="λ_a0")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
