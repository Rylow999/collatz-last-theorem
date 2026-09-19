# Parte 1: The Divergence Threshold of the Collatz Map

**A Conditional Closed-Form Necessary Condition** (julio 2026)

Este directorio contiene el PASO 1 del programa (el umbral condicional),
conservado tal como fue publicado en su momento:

- `paper/collatz_divergence_threshold.tex` — el LaTeX original
- `code/collatz_simulation.py` — el simulador de órbitas (25.000 órbitas)
- `data/collatz_orbits_50000.csv` — los datos crudos

## El resultado

**Teorema (condicional a LEH):** si una órbita diverge sub-exponencialmente,
entonces f_P ≥ f_P* = log₄(8/3) = 0.7075.

- La identidad **μ_P + μ_N = -2** está probada incondicionalmente.
- LEH (equidistribución local por-órbita) es el ingrediente no probado.

**Este documento es el PASO 1** del programa completo (ver README raíz):
umbral condicional → evidencia numérica → acotación → corolario.
