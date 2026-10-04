#!/usr/bin/env python3
# exp_margen_vs_L.py - curva margen-vs-L: la uniformidad del margen joint
# (bache #2 del paper). Metodologia SDDF: ventanas DECLARADAS (prefijos
# anidados de las mismas orbitas), n0 enorme (10^15..10^16) para que ninguna
# orbita termine dentro de L_max: la dependencia con la longitud se mide en
# segmentos genuinamente largos.
# margen = thr(g_N) - f_P > 0  <=>  f_P por debajo del umbral (contractivo).
# nN == 0 (todas P, f_P=1): margen = -1 (en region de divergencia).
# Salida: data/margen_vs_L.json
import numpy as np
import random
import json
import time
from pathlib import Path

L3 = np.log2(3)
CHECKPOINTS = [500, 2000, 5000, 20000]
L_MAX = 20000
N_ORBITS = 1000

def nu2(n):
    v = 0
    while n % 2 == 0 and n > 0:
        n //= 2
        v += 1
    return v

def main():
    t0 = time.time()
    rng = random.Random(2026)
    mins = {}
    meds = {}
    viol = {}
    for L in CHECKPOINTS:
        mins[L] = 1e9
        meds[L] = []
        viol[L] = 0
    for oi in range(N_ORBITS):
        if oi % 100 == 0:
            print(f"  orbita {oi}...", flush=True)
        n0 = rng.randrange(10**15 + 1, 10**16, 2)
        n = n0
        nP = 0
        odds = 0
        sum_vN = 0
        nN = 0
        ci = 0
        for step in range(1, L_MAX + 1):
            if n <= 1:
                break   # FIX 2026-10-03: la orbita convergio; iterar n=1 es el artefacto thr(2)
            if n % 2 == 1:
                odds += 1
                m = 3 * n + 1
                v = nu2(m)
                if n % 4 == 3:
                    nP += 1
                else:
                    nN += 1
                    sum_vN += v
                n = m >> v
            else:
                n //= 2
            if ci < len(CHECKPOINTS) and step >= CHECKPOINTS[ci]:
                Lc = CHECKPOINTS[ci]   # EXPLICITO: L residual del init loop = bug de sombra
                fP = nP / odds
                if nN == 0:
                    marg = -1.0
                else:
                    gN = sum_vN / nN
                    thr = (L3 - gN) / (1.0 - gN)
                    marg = thr - fP
                meds[Lc].append(marg)
                if marg < mins[Lc]:
                    mins[Lc] = marg
                if marg <= 0:
                    viol[Lc] += 1
                ci += 1
    rows = []
    for L in CHECKPOINTS:
        arr = np.array(meds[L])
        if len(arr) == 0:
            rows.append({"L": L, "n": 0, "margen_min": None, "margen_med": None, "violaciones": 0})
            print(f"L={L:6d}: SIN DATOS", flush=True)
            continue
        rows.append({
            "L": L, "n": len(arr),
            "margen_min": float(arr.min()),
            "margen_med": float(np.median(arr)),
            "violaciones": int((arr <= 0).sum()),
        })
        print(f"L={L:6d}: min={arr.min():+.4f} med={np.median(arr):+.4f} viol={(arr<=0).sum()}", flush=True)
    out = Path(__file__).parent.parent / "data" / "margen_vs_L.json"
    out.write_text(json.dumps({
        "n_orbits": N_ORBITS, "n0_range": "10^15..10^16 (odd)",
        "checkpoints": rows, "tiempo_s": time.time() - t0,
    }, indent=1))
    print("MVL_DONE", flush=True)

if __name__ == "__main__":
    main()
