#!/usr/bin/env python3
# exp_nullrachas.py - null ESTRUCTURADO (rachas exactas iid + v_post por la
# formula exacta) vs COLLATZ real, con matching EXACTO por odd-visits.
#
# Componentes verificados:
#   - rachas: P(racha >= k) = 2^-k (relacion binaria, exp_relacion_binaria)
#     => sampler: l = floor(-log2(u))  [E[l]=1, f_P del null ~ 0.5]
#     (el run anterior tenia el bug "-1": E[l]=0.5, f_P=0.33: null roto)
#   - v_post = 1 + nu2(3^(l+1) j - 1), j impar Haar (4144 pares, 100%)
#   - Collatz real: n0 ~ 10^17..10^18 (orbitas largas, sobreviven O odd-visits)
#
# La pregunta: si Collatz == null estructurado ventana a ventana, la memoria
# del mapa es 0 y la cota viene de la estructura de rachas sola.
import numpy as np
import random
import json
import time
from pathlib import Path

def nu2(n):
    v = 0
    while n % 2 == 0 and n > 0:
        n //= 2
        v += 1
    return v

def null_orbit(O, rng):
    """f_P de una orbita de O odd-visits: rachas iid P(l)=2^-(l+1) + 1 N-visit."""
    odds = 0
    nP = 0
    nN = 0
    sumvN = 0.0
    while odds < O:
        # P(racha >= k) = 2^-k  <=>  l = floor(-log2 u)  (verificado: E[l]=1)
        l = int(np.floor(-np.log2(rng.random())))
        if l > 0:
            take = min(l, O - odds)
            nP += take
            odds += take
            if odds >= O:
                break
        # N-visit con v_post exacta de la formula
        j = 2 * int(rng.integers(0, 10**9)) + 1
        v = 1 + nu2(int(3 ** (l + 1)) * j - 1)
        sumvN += v
        nN += 1
        odds += 1
    fP = nP / odds
    gN = sumvN / nN if nN > 0 else 3.0
    return fP, gN

def real_orbit(n0, O_target):
    """f_P, g_N de una orbita real de O_target odd-visits (None si termina antes)."""
    n = int(n0)
    nP = 0
    odds = 0
    nN = 0
    sumvN = 0.0
    while odds < O_target and n > 1:
        if n % 2 == 1:
            odds += 1
            m = 3 * n + 1
            v = nu2(m)
            if n % 4 == 3:
                nP += 1
            else:
                nN += 1
                sumvN += v
            n = m >> v
        else:
            n //= 2
    if odds < O_target:
        return None
    fP = nP / odds
    gN = sumvN / nN if nN > 0 else 3.0
    return fP, gN

def main():
    F_STAR = np.log(8 / 3) / np.log(4)
    t0 = time.time()
    out = {"f_p_star": F_STAR, "rows": []}
    from scipy import stats as stt
    for O, ntrials in [(100, 40000), (300, 40000), (1000, 20000)]:
        # ----- null estructurado -----
        rng = np.random.default_rng(100 + O)
        nulls = np.array([null_orbit(O, rng)[0] for _ in range(ntrials)])
        # ----- collatz real, mismas longitudes -----
        col = []
        rng2 = random.Random(200 + O)
        tries = 0
        target = min(20000, ntrials)
        while len(col) < target and tries < 1500000:
            tries += 1
            n0 = rng2.randrange(10**17, 10**18, 2)
            fp_gn = real_orbit(n0, O)
            if fp_gn is not None:
                col.append(fp_gn[0])
        if len(col) < 1000:
            print(f"O={O}: solo {len(col)} orbitas en {tries} intentos - omitido", flush=True)
            continue
        arr = np.array(col)
        ks = stt.ks_2samp(arr, nulls)
        row = {
            "O": O,
            "n_null": int(ntrials), "n_collatz": int(len(arr)), "tries": int(tries),
            "null_med": float(np.median(nulls)), "null_max": float(nulls.max()),
            "null_gt_fpstar": float(np.mean(nulls > F_STAR)),
            "collatz_med": float(np.median(arr)), "collatz_max": float(arr.max()),
            "collatz_gt_fpstar": float(np.mean(arr > F_STAR)),
            "ks_D": float(ks.statistic), "ks_p": float(ks.pvalue),
        }
        out["rows"].append(row)
        print(f"O={O}: null med={row['null_med']:.4f} max={row['null_max']:.4f} P>f*={row['null_gt_fpstar']:.2e}", flush=True)
        print(f"      coll med={row['collatz_med']:.4f} max={row['collatz_max']:.4f} P>f*={row['collatz_gt_fpstar']:.2e}", flush=True)
        print(f"      KS D={row['ks_D']:.4f} p={row['ks_p']:.3g}", flush=True)
    out["tiempo_s"] = time.time() - t0
    Path(__file__).parent.parent.joinpath("data", "nullrachas.json").write_text(json.dumps(out, indent=1))
    print("NR_DONE", flush=True)

if __name__ == "__main__":
    main()
