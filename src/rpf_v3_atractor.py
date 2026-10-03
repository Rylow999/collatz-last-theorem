#!/usr/bin/env python3
"""
RPF v3 — refinamiento: m hasta 10, restriccion al atractor y tendencia del gap.

Cambios respecto a v2:
1. Estados SOLO los alcanzables: impares no divisibles por 3 (las filas
   x≡0 mod 3 tienen masa 0 — T nunca cae en multiplos de 3, asi que esos
   estados son transientes; el operador vive sobre el atractor).
   OJO: las preimagenes y=(2^k x-1)/3 SI pueden ser multiplo de 3
   (columnas), pero en la siguiente iteracion L mata esa masa. El
   espectro relevante es el de L restringida a estados no-divisibles:
   sub-matriz P = L[A,A] donde A = {impares, no ≡0 mod 3}.
2. m hasta 10 (N util ~ 341 estados en m=10) con eig denso.
3. Normalizacion: el espectro crudo tiene lambda1 que depende de la
   masa; para el GAP usamos lambda2/lambda1 (invariante de escala).
"""
import numpy as np
import json
from pathlib import Path

def build_L_full(m, K=26):
    N = 2**m
    impares = list(range(1, N, 2))
    idx = {s: i for i, s in enumerate(impares)}
    L = np.zeros((len(impares), len(impares)))
    for x in impares:
        r = x % 3
        if r == 0:
            continue
        ks = range(2, K+1, 2) if r == 1 else range(1, K+1, 2)
        for k in ks:
            y = ((2**k) * x - 1) // 3
            L[idx[x], idx[y % N]] += 2.0**(-k)
    return L, impares

def main():
    print("="*74)
    print("RPF v3: atractor (no-0mod3), tendencia del gap hasta m=10")
    print("="*74)
    rows = []
    for m in (4, 5, 6, 7, 8, 9, 10):
        L_full, impares = build_L_full(m)
        # atractor: impares no divisibles por 3
        A = [s for s in impares if s % 3 != 0]
        ia = [impares.index(s) for s in A]
        P = L_full[np.ix_(ia, ia)]
        row_mass = P.sum(axis=1)
        col_mass = P.sum(axis=0)
        w = np.linalg.eigvals(P)
        w_abs = np.sort(np.abs(w))[::-1]
        l1, l2, l3 = w_abs[0], w_abs[1], w_abs[2]
        rows.append({
            "m": m, "N_atractor": len(A),
            "row_mass_min": float(row_mass.min()),
            "row_mass_max": float(row_mass.max()),
            "row_mass_mean": float(row_mass.mean()),
            "col_mass_min": float(col_mass.min()),
            "lambda1": float(l1), "lambda2": float(l2), "lambda3": float(l3),
            "gap_rel": float(1 - l2/l1),
        })
        print(f"m={m:2d} |A|={len(A):4d}  l1={l1:.4f} l2={l2:.4f} l3={l3:.4f} "
              f" gap={1-l2/l1:.4f}  masa fila [{row_mass.min():.3f},{row_mass.max():.3f}] "
              f" col_min={col_mass.min():.4f}")

    out = Path(__file__).parent.parent / "data" / "rpf_v3_atractor.json"
    out.write_text(json.dumps(rows, indent=1))
    print(f"\nGuardado: {out}")

if __name__ == "__main__":
    main()
