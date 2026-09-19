# Collatz Last Theorem

**Convirtiendo la Conjetura de Collatz en un corolario de la acotación de la desviación de equidistribución.**

Autor: Luciano Benjamín Nieto · Asistencia: Nexus (agente)
Licencia: CC-BY 4.0

---

## La idea en una página

La Conjetura de Collatz (toda órbita del mapa 3n+1 alcanza 1) sigue abierta
porque ninguna verificación finita puede cerrar un enunciado sobre todos los
enteros. Pero el programa LOGOS/COLLATZ
([`Rylow999/vega-vault/LOGOS/COLLATZ`](https://github.com/Rylow999/vega-vault))
ya derivó un **umbral condicional exacto**:

$$f_P^* = \log_4(8/3) = 0.7075$$

**Teorema (probado, condicional a LEH):** si una órbita diverge
sub-exponencialmente, entonces su frecuencia de visitas a la clase
P = {n ≡ 3 mod 4} cumple f_P ≥ f_P* durante toda la órbita.

**Este repositorio busca el paso que falta:** demostrar que esa condición
**nunca se cumple** — es decir, la **acotación**:

$$|f_P - \mu| \leq C \quad \text{para toda órbita, con } C < f_P^* - \mu$$

donde μ ≈ 0.324 es la media empírica de f_P (la medida invariante del mapa).
Si la acotación vale con C < 0.374, la conjetura cae como corolario:
**ninguna órbita puede sostener f_P ≥ 0.7075, luego ninguna diverge**.

## Por qué este enfoque es atacable

1. **Es teoría ergódica estándar**: acotación de la desviación de la medida
   invariante — un enunciado más débil que LEH (equidistribución por-órbita)
   y con herramientas conocidas.
2. **El umbral es exacto y ya derivado** — no depende de ajustes.
3. **El gap es medible**: la evidencia numérica (100k órbitas) muestra que
   Collatz acumula desviación más lento que el azar equivalente, con cola
   corta (0.135%) y sin órbitas divergentes.

## El hallazgo numérico (experimento `exp_theorema.py`)

Con 100.000 órbitas (impares hasta 2M) y null model con la misma estructura
del mapa (P=1/3 + racimos geométricos de N):

| Sistema | Exponente b (|f_P−ref| ~ n^b) |
|---|---|
| CLT naive (Terras simplificado, i.i.d.) | −0.500 |
| **Null (P=1/3 + racimos)** | **−0.472** (el null SÍ cancela como predice CLT) |
| **Collatz vs medida invariante (μ=0.324)** | **−0.264** |
| **GAP** | **+0.21 — Collatz ACUMULA más desviación que el azar** |

**La cola existe**: 135/100.000 órbitas (0.135%) con |f_P−1/3|>0.15 —
y **todas convergen** (ninguna divergencia real hasta n=2M).

**Lectura**: el mapa no es un dado perfecto — tiene "memoria" estructural
que acumula desviación más que el azar. Esa memoria es el **sustrato real**
donde una órbita divergente tendría que vivir. El teorema a buscar es la
**acotación** de esa memoria.

## Estructura del repositorio

```
collatz-last-theorem/
├── README.md                    este archivo
├── docs/
│   └── ESTRATEGIA.md            el camino completo: LEH → acotación → corolario
├── src/
│   ├── collatz_core.py          el mapa, órbitas, estadísticas
│   ├── exp_theorema.py          la evidencia numérica (exponente + cola)
│   ├── exp_acotacion.py         la búsqueda del techo C de la desviación
│   └── exp_null_model.py        el azar con la misma estructura
├── data/                        resultados (JSON/CSV)
├── paper/
│   ├── collatz_last_theorem.tex el paper (LaTeX)
│   └── references.bib
└── figures/                     figuras
```

## Los tres pasos del programa

| Paso | Qué | Estado |
|---|---|---|
| 1. Umbral condicional | f_P* = 0.7075 derivado (cond. LEH) | ✅ probado (repo LOGOS/COLLATZ) |
| 2. Evidencia numérica | la desviación acumula sobre el azar (+0.21), cola 0.135% que converge | ✅ este repo |
| 3. La acotación | \|f_P−μ\| ≤ C < 0.374 para toda órbita | ⬜ **el teorema a buscar** |

Si el paso 3 se demuestra → **la conjetura es un corolario**.

## Repos hermanos

- [`Rylow999/vega-vault/LOGOS/COLLATZ`](https://github.com/Rylow999/vega-vault) — el umbral condicional (paso 1)
- [`Rylow999/rho-law`](https://github.com/Rylow999/rho-law) — el marco unificador (tres capas)
- [`Rylow999/fhrr-rho-collapse`](https://github.com/Rylow999/fhrr-rho-collapse) — la ley ρ en VSA
- [`Rylow999/sddf`](https://github.com/Rylow999/sddf) — turbulencia (Navier-Stokes)

## Falsabilidad

El programa es falsable en ambos sentidos:
- Si aparece una órbita con f_P ≥ 0.7075 sostenido → contraejemplo (conjetura falsa)
- Si la acotación se rompe (existe C > 0.374 necesario) → el camino cerrado
- Si se demuestra la acotación → **conjetura como corolario**

*Per aspera, ad astra.*
