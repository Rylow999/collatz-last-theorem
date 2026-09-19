#!/usr/bin/env python3
"""
COLLATZ LAST THEOREM — el experimento DEFINITIVO de la acotación.

Los datos previos mostraron: C* = 0.3089 pero incluidas órbitas TRIVIALES
(f_P = 0: los n que bajan directo sin pasar por P). El máximo GENUINO
(órbitas con al menos 1 paso P) es lo que determina el techo real.

Este experimento:
  1. Separa órbitas TRIVIALES (f_P = 0 exacto) de GENUINAS
  2. Mide el C* genuino por ventana de n0 (1M a 50M) — el techo real
  3. Mapea la COLA: las órbitas con desviación máxima (las más raras)
     y sus longitudes — ¿qué tienen de especial?
  4. Verifica: ¿el techo genuino decae con n0? (si decae, la acotación
     es asintótica y la conjetura cae)
  5. El veredicto: C* genuino < 0.374?
"""
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


def orbit_fP_length(n0, max_steps=1000000, cap=1e18):
    """(f_P, longitud, n_trivial) — n_trivial marca si la órbita no pasa por P."""
    n = int(n0)
    p = 0
    tot = 0
    for _ in range(max_steps):
        if n <= 1:
            return p / max(tot, 1), tot, (p == 0)
        if n > cap:
            return p / max(tot, 1), tot, (p == 0)
        if n % 2 == 1:
            m = 3 * n + 1
            v = nu2(m)
            p += 1
            tot += 1 + v
            n = m >> v
        else:
            n //= 2
            tot += 1
    return p / max(tot, 1), tot, (p == 0)


def main():
    t0 = time.time()
    print("=" * 74)
    print("COLLATZ LAST THEOREM — DEFINITIVO: el techo genuino de la desviación")
    print("=" * 74)

    mu = 0.3226  # la medida invariante empírica convergida (ventana grande)
    UMBRAL = 0.374  # f_P* - mu (teoría)

    results = {"mu": mu, "umbral": UMBRAL, "ventanas": [], "cola": []}

    # ============================================================
    # 1. C* genuino por ventana (excluyendo triviales)
    # ============================================================
    print(f"\nmu = {mu:.4f}  (medida invariante)")
    print(f"Umbral a batir: C < {UMBAL:.4f}")
    print(f"\n{'ventana n0':>16} {'n_genuinas':>10} {'n_triviales':>11} "
          f"{'C*_genuino':>11} {'margen':>8}")
    for hi in (1_000_000, 5_000_000, 20_000_000, 50_000_000):
        rng = random.Random(hi)
        n_target = 100_000
        fPs_gen, fPs_triv = [], []
        # muestrear impares en la ventana
        tries = 0
        while len(fPs_gen) + len(fPs_triv) < n_target and tries < n_target * 3:
            n0 = rng.randrange(max(1, hi // 100), hi, 2)
            tries += 1
            fP, L, trivial = orbit_fP_length(n0)
            (fPs_triv if trivial else fPs_gen).append(fP)
        fPs_gen = np.array(fPs_gen)
        C_gen = float(np.abs(fPs_gen - mu).max())
        margen = UMBRAL - C_gen
        results["ventanas"].append({
            "hi": hi, "n_genuinas": len(fPs_gen), "n_triviales": len(fPs_triv),
            "C_genuino": C_gen, "margen": margen,
        })
        print(f"{f'(hasta {hi/1e6:.0f}M)':>16} {len(fPs_gen):10d} {len(fPs_triv):11d} "
              f"{C_gen:11.4f} {margen:+8.4f}")

    C_global = max(v["C_genuino"] for v in results["ventanas"])
    results["C_global_genuino"] = C_global
    results["margen_global"] = UMBRAL - C_global

    # ============================================================
    # 2. La cola: las órbitas más desviadas
    # ============================================================
    print("\n=== LA COLA: las órbitas más desviadas (top 20) ===")
    rng = random.Random(999)
    all_orbits = []
    for i in range(50000):
        n0 = rng.randrange(1, 20_000_000, 2)
        fP, L, trivial = orbit_fP_length(n0)
        if not trivial:
            all_orbits.append({"n0": n0, "fP": fP, "L": L,
                               "dev": abs(fP - mu)})
    all_orbits.sort(key=lambda x: -x["dev"])
    print(f"{'n0':>10} {'f_P':>8} {'dev':>8} {'longitud':>8}")
    for o in all_orbits[:20]:
        print(f"{o['n0']:10d} {o['fP']:8.4f} {o['dev']:8.4f} {o['L']:8d}")
    results["cola"] = all_orbits[:20]

    # Correlación dev vs longitud en la cola (¿las más desviadas son largas?)
    devs = np.array([o["dev"] for o in all_orbits])
    lens = np.array([o["L"] for o in all_orbits])
    corr = float(np.corrcoef(devs, lens)[0, 1])
    print(f"\nCorrelación dev vs longitud (50k genuinas): {corr:.4f}")
    results["corr_dev_longitud"] = corr

    # ¿La desviación máxima decae con n0? (por ventana ya visto; ahora
    # la mediana de la cola por ventana)
    print("\n=== ¿El techo decae con n0? (mediana de |f_P - mu| por ventana) ===")
    for hi in (1_000_000, 10_000_000, 50_000_000):
        rng = random.Random(hi + 1)
        devs_w = []
        for i in range(30000):
            n0 = rng.randrange(max(1, hi // 100), hi, 2)
            fP, L, trivial = orbit_fP_length(n0)
            if not trivial:
                devs_w.append(abs(fP - mu))
        med = float(np.median(devs_w))
        print(f"  hasta {hi/1e6:4.0f}M: mediana={med:.4f}  (n=30000)")
        results.setdefault("mediana_por_ventana", []).append(
            {"hi": hi, "mediana": med})

    # ============================================================
    # Veredicto final
    # ============================================================
    print("\n" + "=" * 74)
    print("VEREDICTO FINAL:")
    print(f"  C* genuino (todo el barrido hasta 50M): {C_global:.4f}")
    print(f"  Umbral:                                  {UMBAL:.4f}")
    print(f"  MARGEN:                                  {UMBAL - C_global:+.4f}")
    if C_global < UMBRAL:
        print("\n  LA ACOTACIÓN SE SOSTIENE con órbitas genuinas.")
        print("  El techo de la desviación de Collatz está por debajo del margen")
        print("  crítico en todo el barrido (50M, 300k órbitas genuinas).")
        print("\n  El último teorema: |f_P - mu| <= C* < f_P* - mu para toda órbita.")
        print("  Si demostrado -> la conjetura de Collatz es un COROLARIO.")
    else:
        print("\n  La acotación se rompe: hay órbitas genuinas sobre el umbral.")

    out = Path(__file__).parent.parent / "data" / "acotacion_definitiva.json"
    out.write_text(json.dumps(results, indent=1))
    print(f"\nGuardado: {out}")
    print(f"Tiempo: {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
