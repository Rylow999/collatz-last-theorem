#!/usr/bin/env python3
"""
Collatz Divergence Threshold — Simulation Engine
Author: Luciano Benjamín Nieto
Date: 2026-07-25

Computes P/N frequencies for all odd starting points n <= MAX_N under the
accelerated Collatz map R(n) = (3n+1) / 2^{nu_2(3n+1)}.

Outputs:
    - collatz_orbits_50000.csv : raw data per orbit
    - collatz_simulation_summary.txt : statistical summary
"""

import csv
import numpy as np
from collections import Counter

MAX_N = 50_000


def collatz_accelerated(n: int, max_steps: int = 100_000):
    """
    Accelerated Collatz map for odd n.
    Returns:
        odd_sequence: list of odd iterates (including n)
        pn_sequence: list of 'P'/'N' classifications
        terminated_by_limit: True if the loop hit max_steps without reaching 1
            (i.e. the orbit was truncated and its f_P is not the true, full-orbit
            value). Callers MUST check this flag before trusting f_P for a given n.
    """
    odd_sequence = [n]
    pn_sequence = []
    current = n
    steps = 0

    while current != 1 and steps < max_steps:
        # Classification
        if current % 4 == 3:
            pn_sequence.append('P')
        else:
            pn_sequence.append('N')

        # Apply accelerated map
        val = 3 * current + 1
        nu = 0
        temp = val
        while temp % 2 == 0:
            temp //= 2
            nu += 1
        current = temp

        if current % 2 == 1:
            odd_sequence.append(current)

        steps += 1

    terminated_by_limit = (current != 1)
    return odd_sequence, pn_sequence, terminated_by_limit


def main():
    log2_3 = np.log2(3)
    f_P_star = (3 - log2_3) / 2

    results = []
    print(f"Simulating orbits for odd n <= {MAX_N}...")

    for n in range(1, MAX_N + 1, 2):
        odd_seq, pn_seq, terminated_by_limit = collatz_accelerated(n)
        K = len(pn_seq)
        f_P = pn_seq.count('P') / K if K > 0 else 0.0

        results.append({
            'n': n,
            'K': K,
            'f_P': round(f_P, 6),
            'orbit_length': len(odd_seq),
            'terminated_by_limit': terminated_by_limit,
            'pn_sequence': ''.join(pn_seq)
        })

    # Statistics
    # Orbits terminated by the step limit have an f_P computed only over a
    # truncated prefix, not the true full orbit -- they must not be used to
    # bound f_P or to claim "no orbit exceeds f_P*".
    n_truncated = sum(1 for r in results if r['terminated_by_limit'])
    complete = [r for r in results if not r['terminated_by_limit']]
    f_P_values = [r['f_P'] for r in complete]
    max_fP = max(f_P_values)
    max_fP_n = complete[f_P_values.index(max_fP)]['n']
    mean_fP = np.mean(f_P_values)
    exceed = sum(1 for fp in f_P_values if fp >= f_P_star)

    # Autocorrelation
    autocorrs = []
    for r in results:
        pn = r['pn_sequence']
        if len(pn) >= 3:
            binary = np.array([1 if x == 'P' else 0 for x in pn])
            corr = np.corrcoef(binary[:-1], binary[1:])[0, 1]
            if not np.isnan(corr):
                autocorrs.append(corr)
    mean_autocorr = np.mean(autocorrs) if autocorrs else 0.0

    # Summary
    summary = f"""# Collatz Simulation Summary
# Date: 2026-07-25
# Parameters: odd n, 1 <= n <= {MAX_N}, accelerated map R(n)=(3n+1)/2^nu_2(3n+1)
# max_steps per orbit (truncation cap) = 100000
# Total orbits: {len(results)}
# Orbits terminated by step limit (excluded from f_P stats below): {n_truncated}
# f_P* (divergence threshold) = {f_P_star:.10f}
# Mean f_P (complete orbits only) = {mean_fP:.6f}
# Max f_P (complete orbits only) = {max_fP:.6f} (n={max_fP_n})
# Empirical margin below threshold = {f_P_star - max_fP:.6f} ({100*(f_P_star - max_fP)/f_P_star:.2f}%)
# Autocorr lag-1 = {mean_autocorr:.6f}
# Complete orbits with f_P >= f_P*: {exceed}
"""

    with open('collatz_simulation_summary.txt', 'w') as f:
        f.write(summary)

    with open('collatz_orbits_50000.csv', 'w', newline='') as f:
        writer = csv.DictWriter(
            f, fieldnames=['n', 'K', 'f_P', 'orbit_length', 'terminated_by_limit', 'pn_sequence']
        )
        writer.writeheader()
        writer.writerows(results)

    print(summary)
    print("Files saved: collatz_simulation_summary.txt, collatz_orbits_50000.csv")


if __name__ == '__main__':
    main()
