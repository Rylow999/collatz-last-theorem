#!/usr/bin/env python3
"""
Collatz Last Theorem — Paso 3: la búsqueda de la ACOTACIÓN.

El teorema a demostrar:
    |f_P - mu| <= C para toda orbita, con C < f_P* - mu = 0.374
    (mu ~ 0.324 medida invariante empirica)

Si la acotacion vale con C < 0.374 -> la conjetura de Collatz es un
corolario: ninguna orbita puede sostener f_P >= f_P* = 0.7075.

Protocolo:
  1. Simular N orbitas impares (barrido de n0 creciente)
  2. Medir el MAXIMO de |f_P - mu| por ventana de n0
  3. Verificar: el maximo se estabiliza (acotado) o crece (sin techo)
  4. Barrer el cap de pasos y la ventana de n0: la acotacion tiene que
     ser robusta a ambos
  5. Buscar el C* empirico: el maximo global sobre todas las orbitas
  6. Comparar con el null: el maximo del azar con la misma estructura

Criterio de exito: C*_empirico < 0.374 en todo el barrido, robusto a
cap y ventana, Y el maximo del null comparable (para que la acotacion
sea del sustrato, no del azar).
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


def orbit_fP_length(n0, max_steps=200000, cap=1e18):
    n = int(n0)
    p = 0
    tot = 0
    for _ in range(max_steps):
        if n <= 1:
            return p / max(tot, 1), tot
        if n > cap:
            return p / max(tot, 1), tot
        if n % 2 == 1:
            m = 3 * n + 1
            v = nu2(m)
            p += 1
            tot += 1 + v
            n = m >> v
        else:
            n //= 2
            tot += 1
    return p / max(tot, 1), tot


def random_fP(length, seed, pP=1/3):
    rs = np.random.RandomState(seed)
    nP = 0
    tot = 0
    while tot < length:
        if rs.rand() < pP:
            nP += 1
            tot += 1 + rs.geometric(0.5)
        else:
            tot += 1
    return nP / max(tot, 1)


def main():
    t0 = time.time()
    print("=" * 72)
    print("COLLATZ LAST THEOREM — Paso 3: la busqueda de la ACOTACION")
    print("=" * 72)
    print("Teorema a demostrar: |f_P - mu| <= C < 0.374 para toda orbita")
    print("(mu ~ 0.324; si C < 0.374, la conjetura es un corolario)\n")

    rng = random.Random(42)

    # ============================================================
    # 1. Barrido por ventana de n0 (el maximo se estabiliza?)
    # ============================================================
    print("PASO 1: el maximo de |f_P - mu| por ventana de n0")
    print(f"{'ventana n0':>14} {'n_orbitas':>9} {'max|f_P-mu|':>12} {'C vs 0.374':>10}")
    windows = [(1, 1_000), (1, 10_000), (1, 100_000), (1, 1_000_000), (1, 5_000_000)]
    mu_est = None
    window_results = []
    for lo, hi in windows:
        n0s = list(range(lo, hi + 1, 2))[:200000]  # cap de orbitas por ventana
        fPs = []
        for n0 in n0s:
            fP, _ = orbit_fP_length(n0, max_steps=100000)
            fPs.append(fP)
        fPs = np.array(fPs)
        if mu_est is None:
            mu_est = float(fPs.mean())  # primera ventana calibra mu
        dev = np.abs(fPs - mu_est)
        C_emp = float(dev.max())
        ok = C_emp < 0.374
        window_results.append({
            "lo": lo, "hi": hi, "n": len(n0s),
            "mu_window": float(fPs.mean()), "C_empirical": C_emp,
            "acotada": bool(ok),
        })
        print(f"{f'[{lo}-{hi}]':>14} {len(n0s):9d} {C_emp:12.4f} "
              f"{'SI' if ok else 'NO':>10}")

    print(f"\n  mu (medida invariante empirica): {mu_est:.4f} (teoria 1/3)")
    all_acotada = all(w["acotada"] for w in window_results)
    C_global = max(w["C_empirical"] for w in window_results)
    print(f"  C* empirico global: {C_global:.4f}  (umbral a batir: 0.374)")
    print(f"  ACOTADA en todas las ventanas: {all_acotada}")

    # ============================================================
    # 2. Robustez al cap de pasos
    # ============================================================
    print("\nPASO 2: robustez al cap de pasos (las orbitas largas)")
    cap_results = []
    for max_steps in (1000, 10000, 100000, 500000):
        fPs = []
        n0s = [rng.randrange(1, 2_000_000, 2) for _ in range(30000)]
        for n0 in n0s:
            fP, _ = orbit_fP_length(n0, max_steps=max_steps)
            fPs.append(fP)
        fPs = np.array(fPs)
        dev = np.abs(fPs - mu_est)
        C_emp = float(dev.max())
        # cuantas orbitas fueron truncadas (no convergieron dentro del cap)
        # aproximamos: las que tienen length == max_steps
        cap_results.append({
            "max_steps": max_steps, "C_empirical": C_emp,
            "mu_window": float(fPs.mean()),
        })
        print(f"  cap={max_steps:7d}: max|f_P-mu|={C_emp:.4f} "
              f"(mu ventana={fPs.mean():.4f})")

    # ============================================================
    # 3. Null comparison: el maximo del azar
    # ============================================================
    print("\nPASO 3: null comparison (el maximo del azar con la misma estructura)")
    null_C = 0.0
    for i in range(50000):
        L = int(max(10, lengths_proxy := 40))  # longitud tipica
        fP = random_fP(L, seed=i)
        null_C = max(null_C, abs(fP - mu_est))
    # el null con longitud variable (como las orbitas reales)
    null_C_var = 0.0
    for i in range(50000):
        L = int(min(5000, max(10, 40 * (1 + i % 10))))
        fP = random_fP(L, seed=100000 + i)
        null_C_var = max(null_C_var, abs(fP - mu_est))
    print(f"  Null max|f_P-mu| (long fija 40):   {null_C:.4f}")
    print(f"  Null max|f_P-mu| (long variable):  {null_C_var:.4f}")
    print(f"  Collatz C*:                        {C_global:.4f}")

    # ============================================================
    # Veredicto
    # ============================================================
    print("\n" + "=" * 72)
    print("VEREDICTO:")
    print(f"  C* (Collatz, todo el barrido): {C_global:.4f}")
    print(f"  Umbral a batir:                0.374 (= f_P* - mu)")
    if C_global < 0.374:
        margen = 0.374 - C_global
        print(f"  MARGEN: {margen:.4f} — la acotacion se sostiene en todo el barrido")
        print("  -> Si la acotacion es TEOREMA (|f_P-mu| <= C < 0.374 para toda orbita),")
        print("     la conjetura de Collatz es un COROLARIO.")
    else:
        print("  -> La acotacion se rompe en el barrido: el camino requiere otra via.")
    print(f"\n  Null max: {max(null_C, null_C_var):.4f} — "
          f"{'el null tambien esta acotado' if max(null_C, null_C_var) < 0.374 else 'el null rompe'}")

    out = Path(__file__).parent.parent / "data" / "acotacion_results.json"
    out.write_text(json.dumps({
        "mu_empirical": mu_est,
        "umbral_C": 0.374,
        "C_global": C_global,
        "margen": 0.374 - C_global,
        "acotada_todas_ventanas": all_acotada,
        "windows": window_results,
        "caps": cap_results,
        "null_max_fijo": null_C,
        "null_max_variable": null_C_var,
        "tiempo_s": time.time() - t0,
    }, indent=1))
    print(f"\nGuardado: {out}")


if __name__ == "__main__":
    main()
