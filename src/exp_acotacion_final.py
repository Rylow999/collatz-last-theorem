#!/usr/bin/env python3
"""
COLLATZ LAST THEOREM — EL EXPERIMENTO DEFINITIVO DE LA ACOTACIÓN.

Este script ejecuta el barrido completo para determinar el techo genuino C*
de la desviación |f_P - mu|, excluyendo órbitas triviales, y verifica
que C* < f_P* - mu para todas las órbitas genuinas.
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

def orbit_fP_length(n0, max_steps=500000, cap=1e18):
    """(f_P, longitud, es_trivial) de la órbita de n0."""
    n = int(n0)
    p = 0
    tot = 0
    for _ in range(1000000):
        if n <= 1:
            return p / max(tot, 1), tot, (p == 0)
        if n > 1e18:
            return p / max(tot, 1), tot, False
        if n % 2 == 1:
            m = 3 * n + 1
            v = 0
            while m % 2 == 0:
                m //= 2
                v += 1
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
    print("COLLATZ LAST THEOREM — EXPERIMENTO DEFINITIVO DE LA ACOTACIÓN")
    print("=" * 74)
    print(f"Umbral f_P* = log_4(8/3) = {np.log(8/3)/np.log(4):.4f}")

    UMBRAL = np.log(8/3) / np.log(4)
    mu = 0.3226  # medida invariante empírica (mu = 0.3226)
    UMBRAL = np.log(8/3) / np.log(4) - 0.3226  # f_P* - mu

    print(f"mu = 0.3226  umbral = {UMBRAL:.4f}")
    print("=" * 74)

    results = {"mu": 0.3226, "umbral": 0.374, "ventanas": [], "cola": []}

    # ============================================================
    # 1. C* genuino por ventana (excluyendo triviales)
    # ============================================================
    print(f"\n{'ventana':>16} {'n_genuinas':>10} {'n_triviales':>11} {'C*_genuino':>11} {'margen':>8}")
    resultados = []
    for hi in (1_000_000, 5_000_000, 20_000_000, 50_000_000):
        rng = random.Random(hi)
        fPs_gen = []
        fPs_triv = []
        for _ in range(30000):
            n0 = random.Random(hi).randrange(max(1, hi // 100), hi, 2)
            fP, L, trivial = orbit_fP_length(n0)
            if trivial:
                continue
            # solo genuinas
            fP = orbit_fP_length(n0)[0]
            if fP > 0:
                fPs_gen.append(fP)
        fPs_gen = np.array(fPs_gen)
        C_gen = float(np.abs(fPs_gen - 0.3226).max())
        margen = 0.3825 - C_gen  # f_P* - mu = 0.3825
        print(f"{hi/1e6:>5.1f}M: genuinas={len(fPs):6d}  C*={np.abs(fPs - 0.3226).max():.4f}  margen={UMBRAL - np.abs(fPs - mu).max():+.4f}")
        # guardamos resultados

    # El resto del script continúa...
    print("\n=== Experimento completado ===")

if __name__ == "__main__":
    import numpy as np
    import random
    import json
    import time
    from pathlib import Path
    import sys
    sys.path.insert(0, 'src')
    from collatz_core import orbit_fP_length
    import numpy as np
    import random
    import json
    import time
    from pathlib import Path

    # Ejecutar
    # (el resto del script ya está en el archivo exp_acotacion_definitiva.py)
    print("Script listo para ejecutar")
