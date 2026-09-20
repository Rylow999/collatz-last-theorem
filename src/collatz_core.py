# -*- coding: utf-8 -*-
"""collatz_last_theorem/src/collatz_core.py — El mapa y sus estadísticas.

El núcleo compartido por todos los experimentos:
  - El mapa de Collatz (original y acelerado)
  - Simulación de órbitas con estadísticas de paridad
  - La medida invariante y el umbral condicional
"""
import numpy as np


def nu2(n):
    """Exponente de 2 en n (2-adic valuation)."""
    v = 0
    while n % 2 == 0 and n > 0:
        n //= 2
        v += 1
    return v


def collatz_step(n):
    """Un paso del mapa original: n/2 si par, 3n+1 si impar."""
    return n // 2 if n % 2 == 0 else 3 * n + 1


def orbit_fP_length(n0, max_steps=200000, cap=1e18):
    """(f_P, longitud) de la órbita de n0 bajo el mapa acelerado.

    f_P = pasos_P / pasos_totales, donde cada paso P (impar) trae un
    racimo de pasos N (divisiones por 2). Cuenta los pasos del mapa
    acelerado: 1 P + nu2(3n+1) N por iteración impar.
    """
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


def orbit_sequence(n0, max_steps=2000):
    """La secuencia de pasos (tipo, valor) y los valores de la órbita."""
    n = int(n0)
    seq = []
    values = [n]
    for _ in range(max_steps):
        if n <= 1:
            break
        if n % 2 == 1:
            m = 3 * n + 1
            v = nu2(m)
            seq.append(('P', n))
            for _ in range(v):
                seq.append(('N', m))
                m //= 2
            n = m
        else:
            n //= 2
            seq.append(('N', n))
        values.append(n)
    return seq, values


# ================================================================
# Las constantes del programa (derivadas, no ajustadas)
# ================================================================

# El umbral condicional (paso 1 del programa, LOGOS/COLLATZ)
F_P_STAR = np.log(8 / 3) / np.log(4)  # log_4(8/3) = 0.7075

# El drift 2-adico exacto por paso P (probado, incondicional)
DRIFT_P = np.log2(3) - 2  # -0.415

# La medida invariante empírica (medida en 10^6 órbitas, exp_teorema_final.py)
MU_EMPIRICAL = 0.325035

# El techo genuino de la desviación (exp_acotacion_definitiva.py)
C_STAR_GENUINE = 0.2816

# El margen (umbral - techo)
MARGIN = F_P_STAR - MU_EMPIRICAL - C_STAR_GENUINE  # +0.10


def resumen():
    """Las constantes del programa, imprimidas."""
    print(f"Umbral condicional f_P* = log_4(8/3) = {F_P_STAR:.4f}")
    print(f"Drift 2-adico por paso P = log2(3)-2 = {DRIFT_P:+.4f}")
    print(f"Medida invariante empirica mu = {MU_EMPIRICAL:.6f}")
    print(f"Techo genuino C* = {C_STAR_GENUINE:.4f}")
    print(f"Margen (f_P* - mu - C*) = {F_P_STAR - MU_EMPIRICAL - C_STAR_GENUINE:+.4f}")


if __name__ == "__main__":
    resumen()
