# src/sweep3d.py

#!/usr/bin/env python3
"""
sweep3d.py

2-D sweep of base vs acid for 3D clearing → CSV of (λ_b, λ_a0, mean_h, rms_h)

Defaults chosen to span four decades and hit mean height ≃50 layers:
  λ_b, λ_a0 ∈ [1,2,3,4,16,32,64,128,200,256,350,375,400,450,460,475,500,525,550,1028,2048]
  attenuation length L = 2 layers (0.9 nm voxels → 1.8 nm 1/e depth)
  grid = 256×256×256
  output → data/3d/sweep3d_results.csv
"""

import os
import csv
import argparse
import numpy as np
from simulation3d import simulate_3d

def main():
    parser = argparse.ArgumentParser(description="Sweep λ_b vs λ_a0 for 3D roughness")
    parser.add_argument(
        "-b","--lambda-b",
        nargs="+", type=float,
        default=[1,2,3,4,16,32,64,128,200,256,350,375,400,450,460,475,500,525,550,1028,2048],
        help="List of base means λ_b"
    )
    parser.add_argument(
        "-a","--lambda-a0",
        nargs="+", type=float,
        default=[1,2,3,4,16,32,64,128,200,256,350,375,400,450,460,475,500,525,550,1028,2048, 4096, 8192, 10000,12000, 16384, 20000, 25000, 30000, 40000, 50000],
        help="List of surface acid means λ_a0"
    )
    parser.add_argument("--nx",       type=int, default=256, help="grid X size")
    parser.add_argument("--ny",       type=int, default=256, help="grid Y size")
    parser.add_argument("--nz",       type=int, default=256, help="grid Z size")
    parser.add_argument("--atten",    type=float, default=2.0, help="attenuation length (layers)")
    parser.add_argument(
        "--out-csv", default="data/3d/sweep3d_results.csv",
        help="CSV file to write results"
    )
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.out_csv), exist_ok=True)

    with open(args.out_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["lambda_b", "lambda_a0", "mean_h", "rms_h"])

        for lb in args.lambda_b:
            for la in args.lambda_a0:
                H = simulate_3d(
                    nx=args.nx, ny=args.ny, nz=args.nz,
                    lambda_b=lb, lambda_a0=la, atten_len=args.atten
                )
                mean_h = H.mean()
                rms_h  = H.std()
                writer.writerow([lb, la, mean_h, rms_h])
                print(f"λ_b={lb:.0f}, λ_a0={la:.0f} → ⟨H⟩={mean_h:.2f}, RMS={rms_h:.2f}")

    print(f"\n✓ Sweep complete. Results in {args.out_csv}")

if __name__ == "__main__":
    main()
