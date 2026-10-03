#!/usr/bin/env python3
# exp_teorema_generalizado.py - EL PASO RESTANTE: umbral de divergencia
# generalizado POR-ORBITA, condicional SOLO al telescoping (sin LEH).
#
# El teorema 1 del paper (umbral_condicional) fija g_N = 3 (ensemble Haar):
# eso requiere LEH (equidistribucion local). Pero la algebra del telescopo
# deja el umbral GENERALIZADO con la media realizada de la propia orbita:
#
#   drift log2 por visita impar = f_P*(log2(3)-1) + (1-f_P)*(log2(3)-g_N)
#   sub-exponential divergence (en V_{4/3}; el factor 1/log2(4/3) preserva
#   el signo) exige drift >= 0, o sea:
#
#       f_P >= thr(g_N) = (log2(3) - g_N) / (1 - g_N)     [g_N < 1]
#
#   con g_N = 3 se recupera f_P* = 0.7075187 EXACTO (check numerico abajo).
#
# La correccion (3n+1)/n vs 3n: el residuo de la identidad es
# sum_k 1/(3 n_k ln2) sobre la orbita - dominado por la COLA CHICA
# (n pequeno al final: la correccion es O(1), no O(1/n)). Documentado.
#
# Resultado esperado (y hallazgo): la version simple (g_N >= 3 fijo para
# toda orbita) es FALSA por-orbita (g_N fluctua: min 2.41, max 18) - pero la
# condicion JOINT thr(g_N) - f_P > 0 se sostiene en TODAS las orbitas.
#
# Salida: data/teorema_generalizado.json
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

def orbita_stats(n0, L_max=20000):
    # estadisticas del segmento bajo el mapa acelerado R_3 (siempre impar)
    n = int(n0)
    nP = 0; odds = 0; sum_vN = 0; nN = 0
    lr = 0.0
    for _ in range(L_max):
        if n <= 1:
            break
        if n % 2 == 1:
            odds += 1
            m = 3 * n + 1
            v = nu2(m)
            lr += np.log2(m) - v - np.log2(n)
            if n % 4 == 3:
                nP += 1
            else:
                nN += 1
                sum_vN += v
            n = m >> v
        else:
            lr += -1.0
            n //= 2
    fP = nP / max(odds, 1)
    gN = (sum_vN / nN) if nN > 0 else None
    return fP, gN, odds, lr

def main():
    t0 = time.time()
    L3 = np.log2(3)
    F_P_STAR = (3 - L3) / 2
    print("== TEOREMA GENERALIZADO: umbral por-orbita sin LEH ==", flush=True)
    print(f"check LEH: (log2(3)-3)/(1-3) = {(L3-3)/(1-3):.10f} vs f_P* = {F_P_STAR:.10f}", flush=True)

    # 1) verificacion de la identidad por segmento (con la correccion documentada)
    rng = random.Random(11)
    errs = []
    for _ in range(3000):
        n0 = rng.randrange(1000001, 10000000, 2)
        fP, gN, odds, lr = orbita_stats(n0)
        if gN is None:
            continue
        d_pred = fP * (L3 - 1) + (1 - fP) * (L3 - gN)
        d_real = lr / odds
        errs.append(d_real - d_pred)
    errs = np.array(errs)
    print(f"identidad por segmento: err medio={errs.mean():.2e} max|err|={np.abs(errs).max():.2e} (residuo = correccion (3n+1)/n de la cola chica)", flush=True)

    # 2) margen de divergencia por-orbita (150k)
    rng = random.Random(42)
    fPs = []; gNs = []; lengths = []
    for i in range(150000):
        n0 = rng.randrange(1, 5000000, 2)
        fP, gN, odds, lr = orbita_stats(n0)
        if gN is None:
            continue
        fPs.append(fP); gNs.append(gN); lengths.append(odds)
    fPs = np.array(fPs); gNs = np.array(gNs); lengths = np.array(lengths)
    with np.errstate(divide="ignore", invalid="ignore"):
        thr = (L3 - gNs) / (1.0 - gNs)
    margen = thr - fPs
    viol_simple = int((gNs <= (L3 - fPs.max()) / (1 - fPs.max())).sum())
    res = {
        "f_P_star": F_P_STAR,
        "check_leh_exacto": bool(abs((L3 - 3) / (1 - 3) - F_P_STAR) < 1e-12),
        "identidad_err_medio": float(errs.mean()),
        "identidad_err_max": float(np.abs(errs).max()),
        "n_orbitas": int(len(fPs)),
        "f_P_med": float(np.median(fPs)), "f_P_max": float(fPs.max()),
        "g_N_med": float(np.median(gNs)), "g_N_min": float(gNs.min()), "g_N_max": float(gNs.max()),
        "margen_min": float(margen.min()), "margen_med": float(np.median(margen)),
        "violaciones_joint": int((margen < 0).sum()),
        "violaciones_simple_gN_ge3": viol_simple,
        "thr_para_max_fP": float((L3 - fPs.max()) / (1 - fPs.max())),
        "tiempo_s": time.time() - t0,
    }
    print(f"n={res['n_orbitas']} | f_P med={res['f_P_med']:.4f} max={res['f_P_max']:.4f}", flush=True)
    print(f"g_N med={res['g_N_med']:.4f} min={res['g_N_min']:.4f} max={res['g_N_max']:.4f}", flush=True)
    print(f"MARGEN JOINT: min={res['margen_min']:+.4f} med={res['margen_med']:+.4f} | violaciones={res['violaciones_joint']}", flush=True)
    print(f"version simple (g_N>=3 fijo): violaciones={viol_simple} (falsa por-orbita: g_N fluctua)", flush=True)
    print("TG_DONE", flush=True)
    out = Path(__file__).parent.parent / "data" / "teorema_generalizado.json"
    out.write_text(json.dumps(res, indent=1))

if __name__ == "__main__":
    main()
