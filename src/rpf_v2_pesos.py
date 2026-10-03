#!/usr/bin/env python3
"""
RPF v2 — operador de transferencia con pesos naturales 2-adicos.

Fix respecto de v1: la truncacion mod 2^m de la MATRIZ DE CONTADOS dio
gap=1.0 espurio porque casi todas las preimagenes y=(2^k x-1)/3 caen
fuera de la ventana [0, 2^m) — solo ~0.8 ramas sobrevivian y la matriz
quedaba casi de rango 1.

Aqui hacemos lo correcto para una aproximacion de Ulam/cilindros:

  Dominio: Z_2^odd con la medida de Haar.
  Operador RPF con peso w(y) = |T'(y)|_2^{-1} = 2^{-k} en la rama de
  orden k (la derivada 2-adica de T(y)=(3y+1)/2^k es |3|_2 * 2^k -> peso
  inverso 2^{-k}; |3|_2 = 1).

  L f (x) = sum_{ramas y: T(y)=x} 2^{-k(y)} f(y)

Discretizacion: el codominio se discretiza en cilindros mod 2^m.
Cada preimagen y se REDUCE mod 2^m (en Z_2 la reduccion mod 2^m es
exacta y bien definida aunque y>2^m como entero: tomamos y mod 2^m).
La contribucion 2^{-k} cae al cilindro correcto.

  L_m[i, j] = sum_{x in cilindro i} sum_{k paridad(x)} 2^{-k}
              si (2^k x - 1)/3 mod 2^m = j

Pero paridad de k y la suma sobre k par/impar converge:
  sum_{k par} 2^{-k} = 1/(1-1/4) * 2^{-2} = (4/3)(1/4) = 1/3
  sum_{k impar} 2^{-k} = 2^{-1}/(1-1/4) = 2/3
(esperado: 2/3 de la masa de preimagenes son ramas "un paso de racimo
impar", consistente con x mod 3 = 2 -> k impar).

Ademas cada k da UN cilindro de destino distinto (y_k mod 2^m varia
con k). Computamos la distribucion exacta por k hasta k<=K con
convergencia 2^{-K}.

Salida: matriz L_m, espectro, gap, y comparacion con el autovalor 1
(medida invariante de Haar debe ser el fixed point si L preserva masa:
chequeamos sumas de filas).
"""
import numpy as np
import json
from pathlib import Path

def build_L(m, K=24):
    """L[i,j] sobre estados = impares mod 2^m (tamaño 2^{m-1}).

    Para cada x impar en un representante del cilindro, añadimos
    2^{-k} hacia el cilindro destino de y_k = (2^k x - 1)/3 mod 2^m.
    La paridad exigible de k: x%3==1 -> k par; x%3==2 -> k impar;
    x%3==0 no ocurre porque x es impar... ojo: x impar PUEDE ser 0 mod 3
    (p.ej. 3, 9). En ese caso 2^k x - 1 ≡ -1 ≠ 0 mod 3 para todo k ->
    SIN preimagenes (la orbita hacia atras muere; T no es sobreyectivo
    sobre los impares: la imagen de T evita los multiplos de 3? No:
    T(y) = (3y+1)/2^k. 3y+1 ≡ 1 mod 3, dividir por 2^k mod 3 cambia el
    residuo por (-1)^k, asi que T(y) ≡ ±1 mod 3 — NUNCA 0. Los
    multiplos de 3 impares no tienen preimagen. Correcto.)
    """
    N = 2**m
    impares = list(range(1, N, 2))
    idx = {s: i for i, s in enumerate(impares)}
    L = np.zeros((len(impares), len(impares)))
    for x in impares:
        r = x % 3
        if r == 0:
            continue  # sin preimagenes
        ks = range(2, K+1, 2) if r == 1 else range(1, K+1, 2)
        for k in ks:
            y = ((2**k) * x - 1) // 3  # exacto: divisible por construccion
            y_mod = y % N
            if y_mod % 2 == 0:
                continue  # no deberia pasar: y impar siempre
            L[idx[x], idx[y_mod]] += 2.0**(-k)
    return L, impares

def main():
    print("="*72)
    print("RPF v2: pesos 2^{-k}, preimagenes reducidas mod 2^m (exacto en Z_2)")
    print("="*72)

    rows_data = []
    for m in (4, 5, 6, 7, 8):
        L, impares = build_L(m)
        N = len(impares)
        # normalizacion por fila: medida promedio del cilindro
        row_mass = L.sum(axis=1)
        # media y dispersión de la masa por fila (idealmente ~constante)
        w, V = np.linalg.eig(L)
        order = np.argsort(-np.abs(w))
        w_sorted = np.abs(w)[order]
        lam1, lam2 = w_sorted[0], w_sorted[1] if len(w_sorted) > 1 else 0.0
        gap_rel = 1 - lam2/lam1 if lam1 > 0 else float('nan')
        print(f"m={m:2d} N={N:4d}  masa/fila: min={row_mass.min():.4f} "
              f"max={row_mass.max():.4f} media={row_mass.mean():.4f}")
        print(f"        lambda1={lam1:.4f}  lambda2={lam2:.4f}  "
              f"gap relativo={gap_rel:.4f}")
        rows_data.append({
            "m": m, "N": N,
            "row_mass_min": float(row_mass.min()),
            "row_mass_max": float(row_mass.max()),
            "row_mass_mean": float(row_mass.mean()),
            "lambda1": float(lam1), "lambda2": float(lam2),
            "gap_relativo": float(gap_rel),
        })

    out = Path(__file__).parent.parent / "data" / "rpf_v2_pesos.json"
    out.write_text(json.dumps(rows_data, indent=1))
    print(f"\nGuardado: {out}")

if __name__ == "__main__":
    main()
