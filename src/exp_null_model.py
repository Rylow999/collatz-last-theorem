#!/usr/bin/env python3
"""
COLLATZ LAST THEOREM — el null model (el azar con la misma estructura).

El modelo nulo de Tao: random walk con paso P (probabilidad 1/3) seguido
de racimos de N geométricos (Geom(2), media 2). Es la estructura EXACTA
del mapa acelerado bajo la heurística de equidistribución.

Uso: contraste de la desviación de equidistribución entre Collatz real
y el azar con su misma estructura (el control esencial de los ataques).
"""
import numpy as np


def null_fP(length, seed, pP=1/3):
    """f_P de una secuencia random con la estructura del mapa.

    ESTRUCTURA CORRECTA (sin pasos N sueltos): cada ronda es o bien un
    "evento P" (1 paso P + racimo de N geométrico), o bien — con la
    probabilidad complementaria — un paso P NEGATIVO (solo racimo, sin P).
    En el mapa real, todo N viene de un racimo posterior a un P: no hay
    pasos N sueltos. El modelo con "N sueltos" (else branch añadiendo 1 N)
    produce fracción de P = 0.2, no 1/3 — sesga el null.

    Modelo corregido: cada ronda añade 1 P + racimo Geom(2) con prob 1
    (la estructura del mapa acelerado), y la variación viene del racimo.
    f_P = 1/(1+E[racimo]) = 1/3 exacto.
    """
    rs = np.random.RandomState(seed)
    nP = 0
    tot = 0
    while tot < length:
        nP += 1
        racimo = rs.geometric(0.5)  # Geom(2): media 2
        tot += 1 + racimo
    return nP / max(tot, 1)


def null_orbit_stats(length, seed, pP=1/3):
    """(f_P, nP, tot) completos de una secuencia random."""
    rs = np.random.RandomState(seed)
    nP = 0
    tot = 0
    while tot < length:
        if rs.rand() < pP:
            nP += 1
            tot += 1 + rs.geometric(0.5)
        else:
            tot += 1
    return nP / max(tot, 1), nP, tot


if __name__ == "__main__":
    # sanity: la media de f_P debe converger a 1/3
    import statistics
    for L in (100, 1000, 10000):
        vals = [null_fP(L, seed=i) for i in range(2000)]
        print(f"L={L:6d}: f_P medio = {statistics.mean(vals):.4f} (teoria 1/3 = 0.3333)")
