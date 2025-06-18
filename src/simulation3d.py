# src/simulation3d.py

#!/usr/bin/env python3
"""
simulation3d.py

3-D Poisson Monte Carlo of acid/base clearing with depth-dependent acid dose.
Generates a height map H(x,y), then saves H to CSV and prints mean & RMS roughness.

Usage:
    python src/simulation3d.py \
      --nx 256 --ny 256 --nz 256 \
      --lambda-b 4 16 64 256 1024 \
      --lambda-a0 512 \
      --atten 50 \
      --voxel-size 2 \
      --out-dir data/3d_sweep
"""

import os
import csv
import argparse
import numpy as np

def simulate_3d(nx, ny, nz, lambda_b, lambda_a0, atten_len):
    rng = np.random.default_rng()
    # base counts: constant λ_b
    bases = rng.poisson(lam=lambda_b, size=(nz, ny, nx))
    # acid profile: single exp decay with depth
    z = np.arange(nz)
    lam_a = lambda_a0 * np.exp(-z / atten_len)
    # acid counts: Poisson with λ_a(z)
    acids = rng.poisson(lam=lam_a[:, None, None], size=(nz, ny, nx))
    # cleared if acids >= bases
    cleared = acids >= bases

    # compute height map H(x,y): number of consecutive cleared layers from z=0
    mask_false = ~cleared
    # any_false[z,y,x] is True where acid<base
    any_false = mask_false.any(axis=0)     # shape (ny, nx)
    first_false = np.where(
        any_false,
        mask_false.argmax(axis=0),
        nz
    )
    H = first_false  # H[y,x] ∈ [0..nz]
    return H

def main():
    parser = argparse.ArgumentParser(description="3D acid/base clearing sim")
    parser.add_argument("--nx",        type=int,   default=256, help="grid size X")
    parser.add_argument("--ny",        type=int,   default=256, help="grid size Y")
    parser.add_argument("--nz",        type=int,   default=256, help="grid size Z")
    parser.add_argument("--lambda-b",  type=float, nargs="+", required=True,
                        help="list of base means λ_b to sweep")
    parser.add_argument("--lambda-a0", type=float, required=True,
                        help="surface acid mean λ_a0")
    parser.add_argument("--atten",     type=float, default=50.0,
                        help="acid attenuation length (layers)")
    parser.add_argument("--voxel-size", type=float, default=.9,
                        help="voxel edge length (nm)")
    parser.add_argument("--out-dir",   type=str, default="data/3d_sweep",
                        help="folder to write CSV(s)")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    for lb in args.lambda_b:
        H = simulate_3d(
            nx=args.nx, ny=args.ny, nz=args.nz,
            lambda_b=lb,
            lambda_a0=args.lambda_a0,
            atten_len=args.atten
        )

        # compute metrics
        mean_h = H.mean()
        rms   = H.std()

        # save height map as CSV
        fname = f"H_lb{lb:.0f}.csv"
        path  = os.path.join(args.out_dir, fname)
        np.savetxt(path, H, fmt='%d', delimiter=',')
        print(f"✓ Saved height map: {path}")

        # print stats
        print(f"λ_b={lb}: mean height = {mean_h:.3f}, RMS roughness = {rms:.9f}")

if __name__ == "__main__":
    main()
