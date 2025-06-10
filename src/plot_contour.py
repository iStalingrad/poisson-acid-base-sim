import os
import glob
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def find_latest_csv():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    data_dir  = os.path.join(repo_root, "data")
    csv_paths = glob.glob(os.path.join(data_dir, "*", "*.csv"))
    if not csv_paths:
        raise FileNotFoundError(f"No CSV files found under {data_dir!r}")
    return max(csv_paths, key=os.path.getmtime)

def main():
    parser = argparse.ArgumentParser(description="Contour plot of clearing fraction")
    parser.add_argument(
        "--csvfile", "-c",
        default=None,
        help="Path to CSV; if omitted, auto-pick the newest in ../data/"
    )
    parser.add_argument(
        "--out-plot", "-o",
        default=None,
        help="Output filename for the contour PNG"
    )
    args = parser.parse_args()

    # pick CSV
    csvfile = args.csvfile or find_latest_csv()
    print(f"Reading data from: {csvfile}")
    df = pd.read_csv(csvfile)

    # build the grid
    pivot = df.pivot(index="lambda_b", columns="lambda_a", values="clearing_fraction")
    X, Y = np.meshgrid(pivot.columns.values, pivot.index.values)
    Z = pivot.values

    # plot
    plt.figure()
    cp = plt.contourf(X, Y, Z)
    plt.colorbar(cp, label="Clearing fraction")
    plt.xlabel("λₐ (acid mean)")
    plt.ylabel("λ_b (base mean)")
    plt.title("Clearing fraction contour")

    # decide where to save
    out_folder = os.path.dirname(csvfile)
    default_name = "contour_clearing.png"
    out_plot = args.out_plot or os.path.join(out_folder, default_name)

    plt.savefig(out_plot)
    print(f"✓ Contour plot saved to: {out_plot}")
    plt.show()

if __name__ == "__main__":
    main()
