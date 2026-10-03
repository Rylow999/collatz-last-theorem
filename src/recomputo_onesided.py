#!/usr/bin/env python3
# recompute one-sided: el bound simetrico |f_P - mu| <= C falla porque C* lo
# dominan las orbitas triviales f_P=0 (todo-N descenders: el lado EQUIVOCADO).
# El teorema es ONE-SIDED: divergente => f_P SOSTENIDA >= f_P*. Lo que hay que
# acotar es la desviacion SUPERIOR: C+ = max(f_P - mu), no la simetrica.
import numpy as np, random, json, time
from pathlib import Path

def nu2(n):
    v = 0
    while n % 2 == 0 and n > 0:
        n //= 2
        v += 1
    return v

def fP_defB(n0, max_steps=1000000, cap=1e18):
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

t0 = time.time()
F_P_STAR = np.log(8/3)/np.log(4)
rng = random.Random(42)
fPs = []
for i in range(200000):
    n0 = rng.randrange(1, 5_000_000, 2)
    fP, triv = fP_defB(n0)
    if not triv:
        fPs.append(fP)
fPs = np.array(fPs)
mu = float(fPs.mean())
C_plus  = float((fPs - mu).max())
C_minus = float((mu - fPs).max())
umbral  = F_P_STAR - mu
print(f"mu_B={mu:.4f} f_P*={F_P_STAR:.4f} umbral_efectivo={umbral:.4f}")
print(f"C+ (one-sided sup) = {C_plus:.4f}  margen = {umbral - C_plus:+.4f} -> {'SOSTIENE' if C_plus < umbral else 'ROMPE'}")
print(f"C- (one-sided inf) = {C_minus:.4f} (lado equivocado: orbitas f_P=0 triviales)")
print(f"max f_P = {fPs.max():.4f} vs f_P* = {F_P_STAR:.4f}")
rng2 = random.Random(1)
ventanas = []
for hi in (500_000, 1_000_000, 3_000_000, 5_000_000):
    fWs = []
    for i in range(40000):
        n0 = rng2.randrange(1, hi, 2)
        fP, triv = fP_defB(n0)
        if not triv: fWs.append(fP)
    fWs = np.array(fWs)
    Cw = float((fWs - mu).max())
    ventanas.append({"hi": hi, "n": len(fWs), "C_plus": Cw, "margen": umbral-Cw})
    print(f"  hasta {hi/1e6:.1f}M: n={len(fWs)} C+={Cw:.4f} margen={umbral-Cw:+.4f}")
out = Path(__file__).parent.parent / "data" / "recomputo_onesided.json"
out.write_text(json.dumps({
    "mu_B": mu, "f_P_star": F_P_STAR, "umbral_efectivo": umbral,
    "C_plus": C_plus, "margen_one_sided": umbral - C_plus,
    "C_minus": C_minus, "max_fP": float(fPs.max()), "n": len(fPs),
    "ventanas": ventanas, "tiempo_s": time.time()-t0
}, indent=1))
print("ONESIDED_DONE", flush=True)
