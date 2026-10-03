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

### La acotación (`exp_acotacion.py`, 400k órbitas hasta n₀=5×10⁶)

- **C\* genuino = 0.2036–0.25** — robusto al cap de pasos (10³ a 5×10⁵: el
  máximo se ESTABILIZA en 0.2036). El 0.3089 del barrido por ventana incluía
  órbitas triviales con f_P=0 (los n que bajan directo).
- **El margen contra el umbral es +0.124** (0.374 − 0.25) — más holgado.
- **El null también está acotado** (0.234) pero Collatz lo excede: el exceso
  (sustrato real) tiene techo.

### La acotación ONE-SIDED (`recomputo_onesided.py`, 2026-10-02) — el lado correcto

**Corrección fundamental del enfoque:** el bound simétrico |f_P−μ|≤C era el
lado EQUIVOCADO del teorema. El teorema de divergencia es **one-sided**:
divergente ⟹ f_P **sostenida** ≥ f_P*. Lo que hay que acotar es la desviación
SUPERIOR C+ = max(f_P−μ), no la simétrica — C* lo dominan las órbitas triviales
f_P=0 (los descenders todo-N: C−=0.4725 confirma el diagnóstico).

- **C+ = 0.2061 → margen one-sided = +0.0289 ✓** (200k órbitas, def B: μ=0.4725)
- Ventanas one-sided **todas positivas**: +0.0016 (0.5M), +0.0233 (1M), +0.0075 (3M), +0.0310 (5M)
- **max f_P = 0.6786 < f_P\* = 0.7075** — ninguna órbita se acerca al umbral
- El bound simétrico rompe (−0.237): era el lado equivocado, no un problema de la conjetura

**Estado:** la acotación one-sided se sostiene numéricamente en todo el rango
testeado. El paso formal restante: probar C+ < f_P*−μ — cota determinística de
la desviación superior (large deviations one-sided: el ATAQUE 1 ya desarrollado,
ahora apuntado al lado correcto).

### ATAQUE 1 RE-APUNTADO (`ataque1_onesided.py`, 2026-10-02) — el veredicto

Large deviations **ONE-SIDED** con def B — el ataque original testeaba el
bound simétrico (lado equivocado, dominado por triviales f_P=0) con def A
(pasos, no valores impares) y nunca corrió (I_null=None a 10σ).

- **Null (binomial Haar 50/50, tasa KL exacta):** I(c+) = **0.1148/visita**;
  colas exactas por n: 2.1e-2 (n=20), 4.7e-4 (50), 8.3e-7 (100), 1.0e-11 (200);
  **suma Borel-Cantelli (n=10..5000) = 0.0759, finita**.
- **Collatz real (150k órbitas genuinas, longitudes REALES):** **0 violaciones
  one-sided en todas las ventanas** — L~20: 0/54737, L~50: 0/127713,
  L~100: 0/74187, L~200: 0/4979. Supresión de la cola superior ≥ 100×
  respecto de Haar en esas longitudes.
- **Veredicto:** I(c+) > 0 → Σ P_null(n) converge → **P(órbita con f_P
  sostenida > f_P*) = 0 bajo el modelo** (Borel-Cantelli). Y la corrección del
  cuadro viejo: one-sided (el lado que importa), la memoria del mapa
  **suprime** la cola superior — el "gap +0.21, acumula más desviación" era
  lectura del lado simétrico.

**Estado del programa:** el null de Tao está acotado y Collatz está MÁS acotado
que el null en el lado que el teorema necesita. El paso formal restante: la
cota determinística C+ < f_P*−μ (large deviations one-sided rigurosa — la tasa
KL 0.1148/visita es el candidato natural como constante del exponente, con la
colocación de racimos como corrección).

### La serie RPF (`recomputo_defB.py` + `rpf_*.json`) — el operador de transferencia

El complemento ergódico: preimágenes del mapa acelerado por clase mod 3
(`rpf_transfer_operator.json`: pares (preimagen, ν)), pesos de la matriz de
transferencia sobre 2^m estados (`rpf_v2_pesos.json`: λ1 ~ 0.29–0.34; m=4
prácticamente determinística, λ2/λ1 ≈ 0.67 para m≥5), atractor del operador
(`rpf_v3_atractor.json`), y m=11/12 (`rpf_v3_m11_12.json`: N=683/1365, gap
0.069/0.034 — decae ~2^{−m}: consistente con mezcla geométrica). Hipótesis de
trabajo: el gap del operador de transferencia es la cota de mezcla que el
ATAQUE 3 (ergodicidad, tasa 0.054) necesita para el paso determinístico.

### EL PASO RESTANTE: teorema generalizado sin LEH (`exp_teorema_generalizado.py`, 2026-10-02)

**La generalización que cierra el hueco conceptual:** el teorema 1 del paper
umbral_condicional fija ḡ_N = 3 (ensemble Haar) — eso requiere LEH
(equidistribución local, no probada). Pero la álgebra del telescoping deja el
umbral **generalizado por-órbita**, condicional SOLO al telescoping:

$$f_P \geq \mathrm{thr}(\bar g_N) = \frac{\log_2 3 - \bar g_N}{1 - \bar g_N}$$

con ḡ_N la media de ν₂(3n+1) **realizada por la propia órbita** (sobre sus
visitas a N). Con ḡ_N = 3 se recupera f_P* = 0.7075187496 **exacto** (check a
1e-12). La identidad del drift por segmento está verificada en 3000 órbitas
(residuo = la corrección (3n+1)/n vs 3n, dominada por la cola chica — O(1),
no error).

**Resultado (150k órbitas genuinas):**

| cantidad | valor |
|---|---|
| **margen joint thr(ḡ_N) − f_P: mínimo** | **+0.0571** (positivo en TODAS las órbitas) |
| mediana del margen | +0.2116 |
| órbitas en región de divergencia | **0 de 150000** |
| versión simple (ḡ_N ≥ 3 fijo) | **falsa por-órbita** (24924 violaciones: ḡ_N fluctúa 2.41–18) |

**Lectura (hasta dónde llegamos):** cada órbita o tiene f_P bajo o ḡ_N alto —
la compensación joint thr(ḡ_N)−f_P > 0 nunca se viola. El umbral de divergencia
queda condicional **solo al telescoping** (identidad aritmética), sin
equidistribución: LEH se reemplaza por la media realizada de la propia órbita.
Lo que queda formal: enunciar la identidad como lemma (es álgebra directa del
telescopo con la corrección documentada) y el margen como observación — la
cota determinística global C+ sigue siendo el paso abierto (la curva
thr(ḡ_N) explica POR QUÉ el margen one-sided es estable: las órbitas con f_P
alto tienen ḡ_N alto que compensa).

### Formalización en el paper (2026-10-03)

La sección nueva del paper (`paper/collatz_last_theorem.tex`,
`§"The generalized per-orbit threshold (no equidistribution)"`):

- **Lemma (per-orbit drift identity):** la identidad del telescoping con el
  residuo (3n+1)/n documentado — demostración algebraica directa, verificación
  numérica en 3000 órbitas.
- **Theorem (generalized per-orbit threshold):**
  $f_P \geq \mathrm{thr}(\bar g_N) = (\log_2 3 - \bar g_N)/(1 - \bar g_N)$ —
  sin equidistribución; con ḡ_N = 3 recupera f_P* exacto (10⁻¹²).
- **La jerarquía de umbrales:** el MISMO thr(ḡ_N) unifica los tres niveles como
  puntos de una sola curva — álgebra pura (ḡ_N=2 incondicional: 0.4150), LEH
  (ḡ_N=3: f_P*), joint (ḡ_N realizado).
- **Proposition (joint compensation):** margen positivo en 150k órbitas
  (mínimo +0.0571); la versión simple es falsa por-órbita (24924 violaciones).
- **What remains open:** los tres baches enunciados con precisión — (1) la cota
  determinística global, (2) la uniformidad del margen en segmentos largos,
  (3) si la compensación joint y el ceiling decay son el mismo mecanismo.
- PDF recompilado (tectonic, 117 KB).

### La uniformidad del margen (`exp_margen_vs_L.py`, 2026-10-03) — el bache #2 tiene respuesta

Curva margen-vs-L con la metodología SDDF (ventanas declaradas: prefijos
anidados de las MISMAS órbitas, n₀ ∈ [10¹⁵, 10¹⁶] impar para que nadie termine):

| L | margen mínimo | mediana | violaciones |
|---|---|---|---|
| 500 | +0.1822 | +0.3656 | 0 |
| 2000 | +0.3520 | +0.4027 | 0 |
| 5000 | +0.3895 | +0.4101 | 0 |
| 20000 | +0.4086 | +0.4138 | 0 |

**El margen joint CRECE con la longitud y converge a ~0.41** — la compensación
se auto-fortalece: cuanto más corre la órbita, más lejos de la divergencia
queda (la ley de los grandes números empuja f_P y ḡ_N a sus atractores
per-órbita, y el margen se estabiliza en la mediana). La uniformidad del
ínfimo está soportada empíricamente: peor caso +0.18 ya en L=500, tendencia
monótona creciente. Nota honesta: todos los n₀ < 2⁶⁸ son conocidos-convergentes;
lo que se mide acá es la ESTRUCTURA del margen, no la convergencia.

## Estructura del repositorio

```
collatz-last-theorem/
├── README.md                    este archivo (el programa completo)
├── docs/
│   ├── ESTRATEGIA.md            el camino completo: LEH → acotación → corolario
│   └── umbral_condicional/      ← PASO 1: el umbral (paper original, julio 2026)
│       ├── README.md
│       ├── paper/collatz_divergence_threshold.tex
│       ├── code/collatz_simulation.py
│       └── data/collatz_orbits_50000.csv
├── src/
│   ├── collatz_core.py          el mapa, órbitas, estadísticas
│   ├── exp_theorema.py          la evidencia numérica (exponente + cola)
│   ├── exp_acotacion.py         la búsqueda del techo C de la desviación
│   ├── exp_acotacion_definitiva.py  el techo genuino (decae con n0)
│   └── exp_null_model.py        el azar con la misma estructura
├── data/                        resultados (JSON/CSV)
├── paper/
│   ├── collatz_last_theorem.tex el paper (LaTeX)
│   └── references.bib
└── figures/                     figuras
```

**Nota:** los dos repositorios (Divergence Threshold + Last Theorem) están
unificados bajo este repo. El paso 1 se conserva en
`docs/umbral_condicional/` con su historial original.

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
