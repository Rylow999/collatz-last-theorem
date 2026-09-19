#!/usr/bin/env python3
"""
COLLATZ LAST THEOREM — ATAQUE 2: el offset map de Tao (el obstáculo declarado).

Tao (2019): "The main remaining difficulty is to understand the behaviour of
the n-Syracuse offset map F_n: (N+1)^n -> Z[1/2], and more specifically to
analyse the distribution of the random variable F_n(Geom(2)^n) mod 3^k."

El offset map: para una secuencia de racimos a = (a_1, ..., a_n),
    F_n(a) = (3^n * N_0 + c) / 2^{|a|}
donde c es una constante que depende de los a_i. La distribución de
F_n(Geom(2)^n) mod 3^k es lo que controla la 3-adic distribution de la
órbita.

Tao demuestra que es CASI UNIFORME mod 3^k (con error 2^{-c1 n}).
La casi-uniformidad es la LEH que nuestro umbral necesita.

Este experimento:
  1. Implementa F_n (el offset map) exactamente
  2. Simula F_n(Geom(2)^n) mod 3^k para n y k variados
  3. Mide la desviación de la uniformidad (total variation distance)
  4. Verifica la tasa 2^{-c1 n} de Tao
  5. LA PREGUNTA: ¿la desviación decae para TODOS los k, o hay k donde
     se estanca? Si se estanca en algún k, ahí puede vivir una órbita
     que evite la equidistribución.
"""
import numpy as np
import json
import time
from collections import Counter
from pathlib import Path


def syracuse_offset(a_seq, n0=1):
    """F_n(a_seq): el offset del Syracuse map para la secuencia de racimos.

    El Syracuse map: Syr(n) = (3n+1)/2^{nu2(3n+1)}. Para una secuencia de
    racimos a = (a_1,...,a_n), la iteración compuesta es:
        Syr^n(N) = (3^n * N + c(a)) / 2^{|a|}
    donde c(a) depende solo de los racimos (no de N).

    F_n(a) := (3^n * N + c(a)) / 2^{|a|} para N=0 da el "offset":
        F_n(a) = c(a) / 2^{|a|}
    """
    # iterar desde N=0: cada paso es (3*estado + 1)/2^{a_i}
    estado = 0.0
    for a_i in a_seq:
        estado = (3 * estado + 1) / (2 ** a_i)
    return estado


def main():
    t0 = time.time()
    print("=" * 74)
    print("ATAQUE 2: el offset map F_n — la distribución mod 3^k")
    print("=" * 74)

    results = []
    n_trials = 200000

    for n in (2, 4, 8, 16):
        for k in (1, 2, 3, 4):
            # simular F_n(Geom(2)^n) mod 3^k
            counts = Counter()
            for i in range(n_trials):
                a_seq = np.random.geometric(0.5, size=n)  # Geom(2): media 2
                offset = syracuse_offset(a_seq)
                # mod 3^k: el homomorfismo de Z[1/2] a Z/3^k
                # 2 es invertible mod 3^k (2 * 2^{-1} = 1 mod 3^k)
                inv2 = pow(2, -1, 3 ** k)
                # offset es racional con denominador 2^{|a|}: multiplicar por
                # la inversa del denominador mod 3^k
                denom = int(2 ** sum(a_seq))
                # offset mod 3^k = numerador * inversa(denominador) mod 3^k
                # numerador = 3^n * N_0 + c: con N_0=0 es c
                # reconstruir c: c = offset * 2^{|a|} - 3^n * 0 = offset * 2^{|a|}
                c_val = offset * denom
                if c_val == int(c_val):
                    val = int(c_val) % (3 ** k)
                    counts[val] += 1
                else:
                    # no entero: el offset no está en Z[1/2] con denominador
                    # limpio (pasa con a_seq donde los racimos no alcanzan)
                    counts["no_int"] += 1

            total_valid = sum(v for kk, v in counts.items() if kk != "no_int")
            if total_valid < n_trials * 0.5:
                # demasiados no-enteros: saltar
                results.append({"n": n, "k": k, "error": "demasiados no-enteros"})
                continue
            # total variation distance de la uniformidad
            expected = total_valid / (3 ** k)
            tv = 0.5 * sum(abs(counts.get(j, 0) - expected) for j in range(3 ** k)) / total_valid
            results.append({
                "n": n, "k": k, "tv_distance": round(float(tv), 5),
                "total_valid": total_valid,
                "tasa_teorica": round(float(2 ** (-0.5 * n)), 6),
            })
            print(f"  n={n:2d} k={k}: TV={tv:.5f}  (tasa teorica 2^(-n/2)={2**(-0.5*n):.6f})")

    # La pregunta: ¿la TV decae con n para todos los k?
    print("\n=== ¿La desviación decae con n? ===")
    for k in (1, 2, 3, 4):
        sub = [r for r in results if r.get("k") == k and "tv_distance" in r]
        if len(sub) >= 2:
            tvs = [r["tv_distance"] for r in sub]
            decays = all(tvs[i] >= tvs[i+1] for i in range(len(tvs)-1))
            print(f"  k={k}: TV {tvs} — {'DECAE' if decays else 'NO MONÓTONA'}")

    out = Path(__file__).parent.parent / "data" / "ataque2_offset_map.json"
    out.write_text(json.dumps(results, indent=1))
    print(f"\nGuardado: {out}")
    print(f"Tiempo: {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
