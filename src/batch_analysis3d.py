#!/usr/bin/env python3
"""
batch_analysis3d.py

Process every H_*.csv in a folder with analysis3d.py logic.
"""

import os, glob, subprocess, sys

def main():
    repo = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    data_dir = os.path.join(repo, "data", "3d")
    pattern  = os.path.join(data_dir, "H_lb*.csv")
    files    = sorted(glob.glob(pattern))
    if not files:
        print(f"No CSV files found in {data_dir}", file=sys.stderr)
        sys.exit(1)

    for csv in files:
        base   = os.path.splitext(os.path.basename(csv))[0]  # H_lb4, etc.
        folder = os.path.dirname(csv)
        hmap   = os.path.join(folder, f"{base}_heatmap.png")
        surf   = os.path.join(folder, f"{base}_surface.png")
        print(f"→ Processing {csv} → heatmap: {hmap}, surface: {surf}")
        subprocess.run([
            sys.executable, os.path.join(repo, "src", "analysis3d.py"),
            "-i", csv,
            "--out-heatmap", hmap,
            "--out-surface",   surf
        ], check=True)

if __name__ == "__main__":
    main()
