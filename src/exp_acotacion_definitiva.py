#!/usr/bin/env python3
"""
COLLATZ LAST THEOREM — el techo genuino, versión eficiente.

Solo la medición esencial: C* genuino (órbitas no-triviales) por ventana
de n0, con el barrido optimizado (orb char por n0, sin overhead).

Las preguntas:
  1. C* genuino < 0.374 en cada ventana? (la acotación)
  2. El techo decae con n0? (la acotación asintótica)
"""
import numpy as np
import random
import json
import time
from pathlib import Path


def orbit_fP(n0, max_steps=500000, cap=1e18):
    """f_P de la órbita (solo cuenta pasos P del mapa acelerado)."""
    n = int(n0)
    p = 0
    tot = 0
    for _ in range(max_steps):
        if n <= 1:
            return p / max(tot, 1), (p == 0)
        if n > cap:
            return p / max(tot, 1), (p == 0)
        if n % 2 == 1:
            m = 3 * n + 1
            v = 0
            while m % 2 == 0:
                m //= 2
                v += 1
            p += 1
            tot += 1 + v
            n = m
        else:
            n //= 2
            tot += 1
    return p / max(tot, 1), (p == 0)


def main():
    t0 = time.time()
    mu = 0.3226
    UMBRAL = 0.374

    print("=" * 70)
    print("COLLATZ LAST THEOREM: el techo genuino (eficiente)")
    print(f"mu={mu}  umbral={UMBRAL}")
    print("=" * 70)

    results = {"mu": mu, "umbral": UMBRAL, "ventanas": []}
    for hi in (1_000_000, 5_000_000, 20_000_000):
        rng = random.Random(hi)
        fPs_gen = []
        tries = 0
        while len(fPs_gen) < 30000 and tries < 90000:
            n0 = rng.randrange(max(1, hi // 100), hi, 2)
            tries += 1
            fP, trivial = orbit_fP(n0)
            if not trivial:
                fPs_gen.append(fP)
        fPs_gen = np.array(fPs_gen)
        dev = np.abs(fPs_gen - mu)
        C_gen = float(dev.max())
        margen = UMBRAL - C_gen
        results["ventanas"].append({
            "hi": hi, "n_genuinas": len(fPs_gen),
            "C_genuino": C_gen, "margen": margen,
            "dev_mean": float(dev.mean()),
        })
        print(f"hasta {hi/1e6:3.0f}M: genuinas={len(fPs_gen)} "
              f"C*={C_gen:.4f} margen={margen:+.4f} dev_media={dev.mean():.4f}")

    C_global = max(v["C_genuino"] for v in results["ventanas"])
    results["C_global_genuino"] = C_global
    results["margen_global"] = UMBRAL - C_global

    print(f"\nC* genuino global: {C_global:.4f}  margen: {UMBRAL - C_global:+.4f}")
    print("ACOTACIÓN SE SOSTIENE" if C_global < UMBRAL else "SE ROMPE")

    out = Path(__file__).parent.parent / "data" / "acotacion_definitiva.json"
    out.write_text(json.dumps(results, indent=1))
    print(f"Guardado: {out}")
    print(f"Tiempo: {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
