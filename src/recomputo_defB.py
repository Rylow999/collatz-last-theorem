#!/usr/bin/env python3
"""
COLLATZ LAST THEOREM — RECOMPUTO con la f_P CORRECTA (definición B).

El revisor detectó (y confirmé): el paper usaba f_P = pasos_P/(pasos_P+pasos_N)
que da μ=0.3226 y describe los PASOS del mapa acelerado. Pero el teorema
f_P* = log_4(8/3) deriva de drifts μP/μN POR APLICACIÓN de R_3 (por valor
impar visitado). La f_P correcta es la fracción de VALORES IMPARES que
caen en clase P = {n≡3 mod 4}.

Def B: f_P = (# valores impares en P) / (# valores impares visitados)
mu_B ~ 0.4707 (esperado ~0.5 bajo Haar: P y N casi se visitan igual)

RECOMPUTO COMPLETO: mu, ceiling C*, margin, Chernoff, decay.
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

def fP_defB(n0, max_steps=1000000, cap=1e18):
    """f_P = fraccion de valores impares visitados que estan en clase P (n≡3 mod 4)."""
    n = int(n0)
    p = 0; odds = 0
    for _ in range(max_steps):
        if n <= 1: return p/max(odds,1), (odds==0)
        if n > cap: return p/max(odds,1), (odds==0)
        if n % 2 == 1:
            odds += 1
            if n % 4 == 3: p += 1
            m = 3*n+1; v = nu2(m); n = m >> v
        else:
            n //= 2
    return p/max(odds,1), (odds==0)

def main():
    t0 = time.time()
    F_P_STAR = np.log(8/3)/np.log(4)
    print("="*70)
    print("RECOMPUTO CON DEFINICION B (valor impar en clase P)")
    print("="*70)

    rng = random.Random(42)
    fPs, lengths = [], []
    for i in range(200000):
        n0 = rng.randrange(1, 5_000_000, 2)
        fP, trivial = fP_defB(n0)
        if not trivial:
            fPs.append(fP)
    fPs = np.array(fPs)
    mu = float(fPs.mean())
    F_P_STAR = np.log(8/3)/np.log(4)
    dev = np.abs(fPs - mu)
    C_star = float(dev.max())
    margen = F_P_STAR - mu - C_star  # el margen: umbral(mu) - techo
    umbral_efectivo = F_P_STAR - mu
    print(f"n_orbits genuinas: {len(fPs)}")
    print(f"mu_B (correcta) = {mu:.4f}")
    print(f"f_P* = {F_P_STAR:.4f}")
    print(f"margen critico (f_P* - mu) = {umbral_efectivo:.4f}")
    print(f"C* (techo desviacion) = {C_star:.4f}")
    print(f"MARGEN FINAL (f_P*-mu-C*) = {margen:+.4f}")
    print(f"\n  -> {'ACOTACION SE SOSTIENE' if C_star < umbral_efectivo else 'SE ROMPE'}")
    print(f"  -> el revisor tenia razon: mu=0.47 (def B), no 0.32 (def A)")

    # Decaimiento por ventana
    print("\nTecho por ventana (def B):")
    window_results = []
    rng2 = random.Random(1)
    for hi in (500_000, 1_000_000, 3_000_000):
        fPs_w = []
        for i in range(40000):
            n0 = rng2.randrange(1, hi, 2)
            fP, triv = fP_defB(n0)
            if not triv: fPs_w.append(fP)
        fPs_w = np.array(fPs_w)
        C_w = float(np.abs(fPs_w - mu).max())
        window_results.append({"hi":hi, "n":len(fPs_w), "C":C_w})
        print(f"  hasta {hi/1e6:.1f}M: n={len(fPs_w)} C*={C_w:.4f} margen={umbral_efectivo-C_w:+.4f}")

    # Cola: violaciones de |f_P-1/3|>0.15 y de f_P>0.65
    viol1 = int((np.abs(fPs - 1/3) > 0.15).sum())
    viol2 = int((fPs > 0.65).sum())
    print(f"\nCola: |f_P-1/3|>0.15 -> {viol1} ({100*viol1/len(fPs):.4f}%)")
    print(f"     f_P > 0.65 (cerca del umbral) -> {viol2} ({100*viol2/len(fPs):.4f}%)")
    print(f"     max f_P observado = {fPs.max():.4f}")

    out = Path(__file__).parent.parent / "data" / "recomputo_defB.json"
    out.write_text(json.dumps({
        "mu_B": mu, "f_P_star": F_P_STAR,
        "margen_critico": umbral_efectivo, "C_star": C_star,
        "margen_final": margen, "n": len(fPs),
        "window": window_results,
        "cola_1/3_0.15": viol1, "cola_0.65": viol2,
        "max_fP": float(fPs.max()),
        "tiempo_s": time.time()-t0,
    }, indent=1))
    print(f"\nGuardado: {out}")
    print(f"Tiempo: {time.time()-t0:.0f}s")

if __name__ == "__main__":
    main()