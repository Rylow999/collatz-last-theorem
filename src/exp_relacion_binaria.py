#!/usr/bin/env python3
# exp_relacion_binaria.py - LA RELACION BINARIA DE LAS RACHAS (2026-10-03).
#
# HALLAZGO 1 (EXACTO, verificado 8 valores de k, 800+800 candidatos):
#   racha de P de longitud >= k  <=>  n = 2^(k+1) - 1 (mod 2^(k+1))
#   Las rachas de P son EXACTAMENTE los unos finales del binario.
#   (P-steps encadenados: n=3 mod 4 => v=1 => n'=(3n+1)/2; n' in P sii
#    n = 2^(k+1)-1 mod 2^(k+2) por induccion. Los Mersenne 2^k-1 tienen
#    racha k-1 EXACTA - verificado en orbitas reales: 7->2, 31->4,
#    1023->9, 2^40-1->39.)
#
# HALLAZGO 2: densidad P(racha>=k) = 2^-k EXACTA en todo k=1..10 (150k samples,
#   ratio obs/teo = 0.96-1.01): las rachas sueltas siguen Haar PERFECTAMENTE.
#
# HALLAZGO 3 (el que refuta mi hipotesis del mecanismo): NO hay memoria
#   racha->v: E[v | racha] = 3.0 para TODAS las rachas (0..10+), correlacion
#   -0.0095, Spearman -0.027 (p=0.012). La v siguiente es Haar puro.
#
# CORRECCION HONESTA del ATAQUE 1: la "supresion >=100x" es parcialmente
#   artefacto de matching de longitudes: compare 0 violaciones en orbitas de
#   longitudes distribuidas (mediana ~125, ESTRUCTURADAS: las cortas son
#   trayectorias de convergencia, no random walks cortos) contra el null de
#   longitud FIJA 20. El sesgo mu_B=0.4725 vs mu_null=0.5 da factor ~1.8x en
#   la cola (c+: 0.2350 vs 0.2075). El resto es la estructura de las orbitas
#   cortas. El test correcto: matching por longitud + null con la misma
#   estructura de convergencia.
#
# EL MECANISMO REAL (abierto): la supresion de f_P alta sostenida NO esta en
#   las rachas sueltas (Haar) ni en la memoria racha->v (neutra). Esta en la
#   estructura de las trayectorias de convergencia: las orbitas que sostienen
#   f_P alta deben pasar por estados especificos (unos finales) y la
#   convergencia los eyecta. Formalizar: la ocupacion del transitorio.
#
# Salida: data/relacion_binaria.json
import numpy as np
import random
import json
import time
from scipy import stats as st
from pathlib import Path

def nu2(n):
    v = 0
    while n % 2 == 0 and n > 0:
        n //= 2
        v += 1
    return v

def racha_P_desde(n, max_steps=300):
    r = 0
    for _ in range(max_steps):
        if n % 4 == 3:
            m = 3 * n + 1
            if nu2(m) == 1:
                r += 1
                n = m // 2
            else:
                break
        else:
            break
    return r

def pares_racha_v(n0, max_pares=2000):
    n = int(n0)
    racha = 0
    pares = []
    for _ in range(500000):
        if n <= 1:
            break
        if n % 2 == 1:
            m = 3 * n + 1
            v = nu2(m)
            if n % 4 == 3:
                racha += 1
                n = m >> v
            else:
                pares.append((racha, v))
                racha = 0
                n = m >> v
        else:
            n //= 2
        if len(pares) >= max_pares:
            break
    return pares

def main():
    t0 = time.time()
    res = {}

    # HALLAZGO 1: relacion binaria
    verif = {}
    for k in [1, 2, 3, 4, 5, 8, 10, 14]:
        mod = 2 ** (k + 1)
        resid = mod - 1
        ok = True
        rng = np.random.default_rng(100 + k)
        for _ in range(800):
            n = int(resid + mod * rng.integers(1, 10 ** 7))
            if racha_P_desde(n) < k:
                ok = False
                break
        if ok:
            for _ in range(800):
                n = int(rng.integers(1, 10 ** 10)) | 1
                if n % mod != resid and racha_P_desde(n) >= k:
                    ok = False
                    break
        verif[str(k)] = ok
    res["relacion_verificada"] = verif
    res["relacion_exacta"] = all(verif.values())
    print(f"HALLAZGO 1 (relacion binaria): {'EXACTA' if res['relacion_exacta'] else 'FALSA'}", flush=True)

    # HALLAZGO 2: densidad de rachas
    rng = np.random.default_rng(99)
    sample = rng.integers(1, 10 ** 12, size=300000) | 1
    rachas = np.array([racha_P_desde(int(n), 40) for n in sample[:150000]])
    dens = {}
    for k in range(1, 11):
        obs = float((rachas >= k).mean())
        dens[str(k)] = {"obs": obs, "teo_2^-k": 2 ** -k,
                        "ratio": obs / (2 ** -k)}
    res["densidad_rachas"] = dens
    print("HALLAZGO 2 (densidad = 2^-k): ratios", 
          [round(dens[str(k)]["ratio"], 3) for k in range(1, 11)], flush=True)

    # HALLAZGO 3: no memoria racha->v
    rng = random.Random(77)
    pool = []
    for _ in range(150):
        n0 = rng.randrange(1, 10 ** 15, 2)
        pool += pares_racha_v(n0, 2000)
    pool = np.array(pool)
    rr, vv = pool[:, 0], pool[:, 1]
    rho, pv = st.spearmanr(rr, vv)
    res["memoria_racha_v"] = {"n_pares": len(pool), "pearson": float(np.corrcoef(rr, vv)[0, 1]),
                              "spearman": float(rho), "p": float(pv),
                              "E_v_por_racha": {str(r): float(vv[(rr >= a) & (rr <= b)].mean())
                                                 for r, a, b in [(0,0,0),(1,1,1),(2,2,2),(3,3,3),(4,5,4),(6,10,6)]}}
    print(f"HALLAZGO 3 (sin memoria racha->v): spearman={rho:+.4f} (p={pv:.2e})", flush=True)

    # CORRECCION del ataque 1: el factor real del sesgo
    mu_B = 0.4725
    c_col = np.log(8/3) / np.log(4) - mu_B
    c_nul = np.log(8/3) / np.log(4) - 0.5
    from math import erfc, sqrt
    f20_col = 0.5 * erfc((c_col / (0.5 / sqrt(20))) / sqrt(2))
    f20_nul = 0.5 * erfc((c_nul / (0.5 / sqrt(20))) / sqrt(2))
    res["correccion_matching"] = {
        "c_collatz": float(c_col), "c_null": float(c_nul),
        "P_viol_n20_collatz": float(f20_col), "P_viol_n20_null": float(f20_nul),
        "factor_sesgo": float(f20_nul / f20_col),
        "nota": "el factor real del sesgo mu es ~1.8x, no 100x: el resto de la supresion es estructura de orbitas cortas (trayectorias de convergencia)"
    }
    print(f"CORRECCION: factor de sesgo mu = {f20_nul/f20_col:.2f}x (no 100x)", flush=True)

    res["tiempo_s"] = time.time() - t0
    out = Path(__file__).parent.parent / "data" / "relacion_binaria.json"
    out.write_text(json.dumps(res, indent=1))
    print("RB_DONE", flush=True)

if __name__ == "__main__":
    main()
