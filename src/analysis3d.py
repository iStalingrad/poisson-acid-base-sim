# src/analysis3d.py

#!/usr/bin/env python3
"""
analysis3d.py

Load a 3D height map CSV, compute mean & RMS, and render:
  • 2D heatmap of H(x,y)
  • 3D surface plot of H(x,y)

Usage:
    python src/analysis3d.py \
      --input-csv data/3d_sweep/H_lb256.csv \
      --out-heatmap heatmap_lb256.png \
      --out-surface surface_lb256.png
"""

import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def main():
    parser = argparse.ArgumentParser(description="3D height-map analysis")
    parser.add_argument("--input-csv", "-i", required=True,
                        help="Path to height map CSV")
    parser.add_argument("--out-heatmap", "-hmap",
                        default=None,
                        help="Filename for 2D heatmap PNG")
    parser.add_argument("--out-surface", "-surf",
                        default=None,
                        help="Filename for 3D surface PNG")
    args = parser.parse_args()

    H = np.loadtxt(args.input_csv, delimiter=',')

    mean_h = H.mean()
    rms    = H.std()
    print(f"Mean height = {mean_h:.3f}")
    print(f"RMS roughness = {rms:.3f}")

    # determine output folder
    folder = os.path.dirname(args.input_csv)
    heatmap_path = args.out_heatmap or os.path.join(folder, "heatmap.png")
    surface_path = args.out_surface or os.path.join(folder, "surface.png")

    # 2D heatmap
    plt.figure()
    plt.imshow(H, origin='lower', aspect='equal')
    plt.colorbar(label="Height (layers)")
    plt.title("Height map heatmap")
    plt.tight_layout()
    plt.savefig(heatmap_path)
    print(f"✓ Heatmap saved to {heatmap_path}")

    # 3D surface
    nx, ny = H.shape[1], H.shape[0]
    X, Y = np.meshgrid(np.arange(nx), np.arange(ny))
    fig = plt.figure()
    ax  = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, H, rstride=1, cstride=1, linewidth=0, antialiased=False)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Height")
    plt.tight_layout()
    plt.savefig(surface_path)
    print(f"✓ Surface plot saved to {surface_path}")

if __name__ == "__main__":
    main()
