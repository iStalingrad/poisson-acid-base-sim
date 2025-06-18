#!/usr/bin/env python3
"""
contour_sweep3d.py

Reads the 9×14 sweep CSV and draws a contour of mean height vs (λ_b, λ_a0).
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def find_csv():
    # __file__ is src/contour_sweep3d.py
    repo = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    csv_path = os.path.join(repo, "data", "3d", "sweep3d_results_11x14.csv")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Could not find sweep CSV at {csv_path!r}")
    return csv_path

def main():
    csvfile = find_csv()
    df = pd.read_csv(csvfile)

    # pivot so rows=λ_a0, cols=λ_b
    pivot = df.pivot(index="lambda_a0", columns="lambda_b", values="rms_h")
    λ_b = pivot.columns.astype(float)
    λ_a = pivot.index.astype(float)
    B, A = np.meshgrid(λ_b, λ_a)
    Z = pivot.values

    plt.figure(figsize=(8,6))
    cp = plt.contourf(B, A, Z, levels=20, cmap="viridis")
    cbar = plt.colorbar(cp)
    cbar.set_label("RMS roughness σ (layers)", rotation=270, labelpad=15)

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Base loading λ_b")
    plt.ylabel("Surface acid λ_a0")
    plt.title("Contour of RMS Roughness σ (λ_b vs λ_a0)")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
