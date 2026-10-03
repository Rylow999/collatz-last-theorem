#!/usr/bin/env python3
# ataque1_onesided.py - ATAQUE 1 RE-APUNTADO: large deviations ONE-SIDED (def B).
#
# Correcciones de aplicacion sobre ataque1_final.py:
#   (1) teorema ONE-SIDED: divergente => f_P SOSTENIDA >= f_P*. Se testea
#       (f_P - mu_B) > c+, no |f_P-mu| (el lado simetrico lo dominan las
#       orbitas triviales f_P=0; C- = 0.4725).
#   (2) definicion B (per odd visit): mu_B = 0.4725 (la def A media PASOS).
#   (3) c+ = ln(8/3)/ln(4) - mu_B = 0.2350 (la def A usaba 0.3849).
#   (4) I_null EXACTO: binomial Haar 50/50, I(c) = tasa KL:
#       I(c+) = 0.114955/visita; colas exactas n=10..5000; suma BC = 0.076.
#       (El ataque original nunca corrio: I_null=None con el umbral simetrico.)
#   (5) Collatz con LONGITUDES REALES (n de impares visitados por orbita).
#
# Salida: data/ataque1_onesided.json
import numpy as np
import random
import json
import time
from scipy import stats
from pathlib import Path

def nu2(n):
    v = 0
    while n % 2 == 0 and n > 0:
        n //= 2
        v += 1
    return v

def fP_defB(n0, max_steps=2000000, cap=1e18):
    n = int(n0)
    p = 0
    odds = 0
    for _ in range(max_steps):
        if n <= 1:
            return p / max(odds, 1), (odds == 0), odds
        if n > cap:
            return p / max(odds, 1), (odds == 0), odds
        if n % 2 == 1:
            odds += 1
            if n % 4 == 3:
                p += 1
            m = 3 * n + 1
            v = nu2(m)
            n = m >> v
        else:
            n //= 2
    return p / max(odds, 1), (odds == 0), odds

def main():
    t0 = time.time()
    F_P_STAR = np.log(8 / 3) / np.log(4)
    rng = random.Random(42)
    print("== ATAQUE 1 ONE-SIDED (def B) ==", flush=True)
    fPs = []
    lengths = []
    for i in range(150000):
        n0 = rng.randrange(1, 5000000, 2)
        fP, triv, odds = fP_defB(n0)
        if not triv:
            fPs.append(fP)
            lengths.append(odds)
    fPs = np.array(fPs)
    lengths = np.array(lengths)
    mu = float(fPs.mean())
    cplus = F_P_STAR - mu
    print(f"n={len(fPs)} genuinas | mu_B={mu:.4f} | c+={cplus:.4f}", flush=True)

    print("\n[Collatz] violaciones one-sided por longitud real", flush=True)
    rows = []
    for L in [20, 50, 100, 200, 500, 1000, 2000]:
        mm = (lengths >= L / 2) & (lengths <= 2 * L)
        nsel = int(mm.sum())
        if nsel < 50:
            rows.append({"L": L, "n": nsel, "viol": 0, "frac": None})
            print(f"  L~{L:5d}: n={nsel} (sin datos)", flush=True)
            continue
        viol = int(((fPs[mm] - mu) > cplus).sum())
        frac = viol / nsel
        row = {"L": L, "n": nsel, "viol": viol, "frac": frac}
        if frac > 0:
            row["log"] = float(np.log(frac))
        rows.append(row)
        msg = f"  L~{L:5d}: n={nsel:6d} viol={viol:5d} frac={frac:.2e}"
        if frac > 0:
            msg += f" log={np.log(frac):.2f}"
        print(msg, flush=True)

    print("\n[Null] colas binomiales EXACTAS (I(c) = tasa KL)", flush=True)
    I_kl = (0.5 + cplus) * np.log((0.5 + cplus) / 0.5) + (0.5 - cplus) * np.log((0.5 - cplus) / 0.5)
    nrows = []
    total = 0.0
    for n in [10, 20, 50, 100, 200, 500, 1000, 2000, 5000]:
        k_t = int(np.floor((0.5 + cplus) * n)) + 1
        p = stats.binom.sf(k_t - 1, n, 0.5)
        total += p
        nrows.append({"n": n, "P": float(p)})
        print(f"  n={n:5d}: P={p:.3e}", flush=True)
    print(f"  suma BC (n=10..5000) = {total:.4f} (finita)", flush=True)

    print("\n[Veredicto]", flush=True)
    print(f"I(c+) = {I_kl:.6f}/visita > 0 -> sum P_null converge -> P(orbita divergente) = 0 bajo Haar", flush=True)
    I_col = None
    cw = [r for r in rows if r.get("frac") is not None and r["frac"] > 0]
    if len(cw) >= 3:
        xs = [r["L"] for r in cw]
        ys = [np.log(r["frac"]) for r in cw]
        I_col = float(-np.polyfit(xs, ys, 1)[0])
        print(f"I_Collatz(c+) = {I_col:.4f}/visita", flush=True)
        if I_col >= I_kl:
            print("Collatz decae al menos como el azar -> acotacion one-sided consistente", flush=True)
        else:
            print(f"GAP: Collatz decae mas lento (gap={I_kl - I_col:.4f}/visita)", flush=True)

    out = Path(__file__).parent.parent / "data" / "ataque1_onesided.json"
    data = {
        "mu_B": mu, "f_P_star": F_P_STAR, "c_plus": cplus, "n_orbits": len(fPs),
        "collatz_rows": rows, "null_rows": nrows, "I_kl": I_kl,
        "sum_BC": total, "I_collatz": I_col, "tiempo_s": time.time() - t0,
    }
    out.write_text(json.dumps(data, indent=1))
    print("ATT1_DONE", flush=True)

if __name__ == "__main__":
    main()
