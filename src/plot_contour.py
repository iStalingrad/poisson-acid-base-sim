#!/usr/bin/env python3
"""
plot_contour.py

Read the multi-sweep CSV and draw a contour (topographic) plot:
  • x-axis: λ_a (acid means)
  • y-axis: λ_b (base means)
  • contours/color = clearing_fraction
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Contour plot of clearing fraction")
    parser.add_argument(
        "csvfile",
        help="Path to the CSV (lambda_b,lambda_a,clearing_fraction)"
    )
        "--out-plot", "-o",
        default="contour_clearing.png",
        help="Filename for the output PNG"
    )
    args = parser.parse_args()

    # 1) Load
    df = pd.read_csv(args.csvfile)

    # 2) Pivot into a grid
    #    rows = lambda_b, columns = lambda_a, values = clearing_fraction
    pivot = df.pivot(index="lambda_b", columns="lambda_a", values="clearing_fraction")

    # 3) Build mesh
    X, Y = np.meshgrid(pivot.columns.values, pivot.index.values)
    Z = pivot.values

    # 4) Plot contours
    plt.figure()
    # filled contours
    cp = plt.contourf(X, Y, Z)
    plt.colorbar(cp, label="Clearing fraction")
    plt.xlabel("Mean acid per voxel (λₐ)")
    plt.ylabel("Mean base per voxel (λ_b)")
    plt.title("Clearing fraction: contour map")
    plt.tight_layout()

    # 5) Save & show
    plt.savefig(args.out_plot)
    print(f"✓ Contour plot saved to {args.out_plot}")
    plt.show()

if __name__ == "__main__":
    main()
