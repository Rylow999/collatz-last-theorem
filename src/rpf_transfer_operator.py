#!/usr/bin/env python3
"""
RPF sobre Z2 — estudio del operador de transferencia de Ruelle-Perron-Frobenius
del mapa de Collatz acelerado (estudio ANALITICO + verificacion numerica).

El mapa acelerado R_3: Z2^odd -> Z2^odd, R_3(n) = (3n+1)/2^{nu2(3n+1)}.

Operador de transferencia (RPF):
    (L f)(x) = sum_{y: R_3(y)=x} w(y) f(y)

Ramas inversas: y = (2^k x - 1)/3 con la condicion de congruencia:
    2^k x = 1 mod 3  =>  (-1)^k x = 1 mod 3
La paridad de k esta determinada por x mod 3:
    x=1 mod 3: k par
    x=2 mod 3: k impar
    x=0 mod 3: sin preimagen (la rama 3y+1 nunca da multiplo de 3)

Para x con preimagen, hay una rama por cada k en {1,2,3,...} con la
paridad correcta. La rama de orden k tiene derivada 2-adica |2^k/3|_2=2^{-k}.

OBJETIVO: verificar la estructura de las preimagenes y el espectro de una
aproximacion finita (truncando a x mod 2^m), que es la discretizacion del
operador de transferencia. La tasa espectral de la matriz finita aproxima
el gap espectral del operador continuo.
"""
import numpy as np
from collections import defaultdict
import json
from pathlib import Path
import math


def preimagenes(x, max_k=8):
    """Todas las preimagenes y = (2^k x - 1)/3 de x bajo R_3, para k<=max_k."""
    imgs = []
    for k in range(1, max_k+1):
        num = (2**k)*x - 1
        if num % 3 == 0:
            y = num // 3
            # verificar que R_3(y) = x: nu2(3y+1) = k exactamente
            m = 3*y + 1
            v = 0
            while m % 2 == 0:
                m //= 2; v += 1
            if v == k:  # preimagen valida con racimo exactamente k
                imgs.append((y, k))
    return imgs


def matriz_transferencia(m, max_k=8):
    """Matriz finita del operador L sobre los estados x mod 2^m.

    Estados: los 2^(m-1) impares en [0, 2^m). L[f](x) = sum de preimagenes.
    Para una aproximacion uniforme de transferencia (peso de Haar),
    L^T actuara sobre medidas. Usamos la representacion mas natural:
    la matriz de transicion del mapa inducido (cada x va a sus imagenes R_3(x)).

    AQUI: construimos la matriz de preimagenes: M[y -> x] +1 si R_3(y)=x.
    El radio espectral de la "forward" da la entropia; el gap del backward
    (transfer operator) es lo que queremos.
    """
    # estados impares mod 2^m
    states = [n for n in range(1, 2**m, 2)]
    idx = {s: i for i, s in enumerate(states)}
    N = len(states)
    # Matriz de transferencia "backward": P[x -> y] = 1/n_preimagenes(x) si y es preimagen
    P = np.zeros((N, N))
    for x in states:
        imgs = preimagenes(x, max_k)
        if not imgs:
            continue
        for (y, k) in imgs:
            if y in idx:
                P[idx[x], idx[y]] = 1  # x tiene y como preimagen (no normalizado)
    return P, states


def main():
    print("="*72)
    print("RPF: operador de transferencia del mapa de Collatz en Z2")
    print("="*72)

    # 1. Estructura de preimagenes
    print("\n[1] Estructura de preimagenes (paridad de k por x mod 3)")
    for x in (1, 2, 5, 7, 11, 13):
        xmod3 = x % 3
        parity = "par" if x%3==1 else ("impar" if x%3==2 else "ninguna")
        imgs = preimagenes(x, max_k=6)
        ks = [k for (_, k) in imgs]
        print(f"  x={x} (x mod 3 = {xmod3}, k {parity}): preimagenes k={ks}")

    # 2. Matriz de transferencia y espectro
    print("\n[2] Espectro de la matriz finita (truncada mod 2^m)")
    for m in (4, 5, 6):
        P, states = matriz_transferencia(m, max_k=8)
        N = P.shape[0]
        # el gap: autovalores de P
        w = np.linalg.eigvals(P)
        w_abs = np.abs(w)
        w_sorted = np.sort(w_abs)[::-1]
        # la matriz no esta normalizada (multiplicidad), normalizamos
        # por fila para tener un Markov kernel backward
        row_sums = P.sum(axis=1, keepdims=True)
        row_sums[row_sums==0] = 1
        Pn = P / row_sums
        wn = np.linalg.eigvals(Pn)
        wn_sorted = np.sort(np.abs(wn))[::-1]
        gap = 1 - wn_sorted[1] if len(wn_sorted) > 1 else float('nan')
        print(f"  m={m}: N={N} estados, top eigenvalues: "
              f"{[f'{s:.4f}' for s in wn_sorted[:4]]}, gap={gap:.4f}")

    # 3. Entropia topologica (tasa de crecimiento de preimagenes)
    print("\n[3] Crecimiento del numero de preimagenes")
    for m in (4, 5, 6):
        P, _ = matriz_transferencia(m)
        # numero total de preimagenes (peso de la matriz no normalizada)
        total = P.sum()
        print(f"  m={m}: {int(total)} preimagenes (media {total/P.shape[0]:.3f}/estado)")

    # 4. Guardar
    out = Path(__file__).parent.parent / "data" / "rpf_transfer_operator.json"
    example = {str(x): {"x_mod_3": x%3,
                        "preimagenes": [[y,k] for y,k in preimagenes(x,6)]}
               for x in (1,2,5,7,11,13)}
    out.write_text(json.dumps(example, indent=1))
    print(f"\nGuardado: {out}")


if __name__ == "__main__":
    main()