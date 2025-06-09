#!/usr/bin/env python3
"""
simulation.py

Monte Carlo Poisson-based simulation of acid/base clearing in resist voxels.

Each voxel gets a Poisson(λ_b) draw of base molecules and
a Poisson(λ_a) draw of acid molecules.  A voxel is considered
‘cleared’ if acids >= bases.  This script reports the fraction
of voxels cleared.

Usage:
    python simulation.py -b 4 -a 10 -n 1000000
    python simulation.py --lambda-b 4 --lambda-a 10 --num-voxels 500000
    python simulation.py -h
"""

import numpy
import argparse

def simulate(lambda_b: float, lambda_a: float, num_voxels: int) -> float:
    """Run one Monte Carlo trial and return the fraction of cleared voxels."""
    # draw base and acid counts
    bases = numpy.random.poisson(lam=lambda_b, size=num_voxels)
    acids =numpy.random.poisson(lam=lambda_a, size=num_voxels)
    # a voxel clears if acid count >= base count
    cleared = acids >= bases
    return cleared.mean()

def main():
    parser = argparse.ArgumentParser(
        description="Monte Carlo Poisson simulation for acid-base clearing"
    )
    parser.add_argument(
        "-b", "--lambda-b",
        type=float,
        required=True,
        help="Mean number of base molecules per voxel (λ_b)"
    )
    parser.add_argument(
        "-a", "--lambda-a",
        type=float,
        required=True,
        help="Mean number of acid molecules per voxel (λ_a)"
    )
    parser.add_argument(
        "-n", "--num-voxels",
        type=int,
        default=1_000_000,
        help="Number of voxels to simulate (default: 1,000,000)"
    )
    args = parser.parse_args()

    frac = simulate(args.lambda_b, args.lambda_a, args.num_voxels)
    print(f"Clearing fraction: {frac:.6f}")
    print(
        f"Parameters → λ_b={args.lambda_b}, "
        f"λ_a={args.lambda_a}, "
        f"voxels={args.num_voxels}"
    )

if __name__ == "__main__":
    main()
