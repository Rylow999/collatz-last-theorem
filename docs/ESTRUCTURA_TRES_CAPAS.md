# RHO_LAW — La estructura de tres capas: sustrato, observador, instrumento

**Formalización de la tesis unificadora del programa.**
Fecha: 2026-09-18 · Autoría: Luciano (intuición) + Nexus (formalización)

---

## 1. La tesis

Todo sistema de representación/medición tiene **tres capas**:

| Capa | Definición | Collatz | VSA/HRR | Turbulencia | Luz/Color |
|---|---|---|---|---|---|
| **1. Sustrato** | lo que existe sin observador; la estructura irreducible | drift μ_P+μ_N=-2 (identidad, incondicional) | grafo vivo (vitalidad, traza, omega) | campo de velocidad u(x) | longitud de onda λ |
| **2. Observador** | la operación que lee el sustrato y produce un resultado | f_P, drift acumulado, resonator | gram/pinv/pure/MLP | estimador G[u] | color (cualia) |
| **3. Instrumento** | el dispositivo que media el encuentro, con límite de resolución | grilla, ventana, forzado de medición | codebooks, BLK, κ(M) | grilla de N puntos | ojo, retina |

**Tesis central:** el colapso (falla de la medición) vive en las capas 2-3.
La capa 1 es invariante. Un resultado negativo ("la señal no contiene esa
información") puede ser un artefacto de las capas 2-3, no una propiedad de
la capa 1.

## 2. Los tres teoremas de la capa 1 (uno por dominio)

Cada dominio tiene una **identidad algebraica incondicional** en su capa 1:

### VSA/HRR
El espacio es R^N con binding por convolución. La capa 1 es la **ley de
superposición**: bundle = Σ bind(role_i, filler_i). No hay límite de
capacidad en el espacio — la singularidad κ∈[10³,10⁴] es del observador
(inversa de Gram).

### Collatz
El mapa T_3 tiene la identidad **μ_P + μ_N = -2** (probada, incondicional):
el presupuesto dual de los pasos está balanceado por construcción. El drift
por paso P es log₂(3)-2 = -0.415 < 0. La capa 1 es disipativa **por
aritmética**.

### Turbulencia (SDDF)
El balance espectral ∂E/∂t = T - 2νk²E con ∫T dk = 0: la transferencia
redistribuye, la disipación saca. La capa 1 tiene el presupuesto dual
cerrado. El prefactor 25/12 es exacto (derivado, no ajustado).

### El patrón común
Los tres sustratos tienen un **presupuesto dual cerrado** (dos términos con
suma exacta conocida) y **disipativo neto** (el balance favorece el régimen
estable). La divergencia/colapso requeriría que el presupuesto se invierta
localmente de forma sostenida.

## 3. El hueco: ensemble → órbita

En cada dominio, lo que está probado es la afirmación **del ensemble** (o
global), y lo abierto es la afirmación **por-órbita** (o local):

| Dominio | Probado (ensemble) | Abierto (órbita/local) |
|---|---|---|
| Collatz | E[drift] < 0 (casi todas las órbitas casi acotadas, Tao 2019) | cada órbita converge (LEH: equidistribución por-órbita) |
| Turbulencia | regularidad global en 2D; G* acotado en DNS | regularidad global en 3D (Millennium) |
| VSA | el espacio no colapsa (pure funciona en todo el grid) | ningún codebook cae en la banda κ (elegible a priori) |

**El puente es la pregunta matemática exacta de cada dominio:**

- Collatz: ¿existe una medida invariante singulaar no-equidistribuida con
  soporte en una órbita infinita? (≡ LEH falla para alguna órbita)
- NS 3D: ¿existe solución con limsup R(k,t) = 1? (≡ el presupuesto se
  invierte localmente de forma sostenida)
- VSA: dado κ(M) ∈ [10³,10⁴] elegido a mano, ¿colapsa? (sí — pero es
  evitable eligiendo bien)

## 4. Los mecanismos de auto-regulación (capa 1 protege)

Cada dominio tiene un mecanismo que **mantiene el sistema en el régimen
estable** — y es medible:

| Dominio | Mecanismo | Medible como |
|---|---|---|
| Collatz | equidistribución de pasos P (LEH) | f_P → 0.5 (empírico: máx 0.369 en 161 órbitas) |
| Turbulencia | Tercer Motor (G[u] auto-regula la arrugosidad) | G* plateau en DNS 2D |
| VSA | resonator puro (cleanup iterativo sin Gram) | accuracy 1.0 en todo el grid |
| NS 3D (audit Santibañez-Leal) | localización de capas ("lo que mantiene viva la cascada es la localización, no la velocidad") | error de localización λ_q^{-1} |

**La ley de los mecanismos:** ninguno actúa por velocidad; actúan por
**estructura** (equidistribución, localización, iteración limpia). El forzado
que actúa sobre el instrumento (capa 3) no los rompe.

## 5. Los tres tipos de transición (verificados con datos)

| Tipo | Dominio ancla | Firma | Datos |
|---|---|---|---|
| **Puntual** (singularidad de ancho cero) | VSA ρ=1 | accuracy cae y recupera en un punto exacto | Exp 9: 14 valores de ρ, solo 1.000 colapsa |
| **Gradual** (rampa) | Collatz forzado ε | f_P sube suavemente con el forzado | Exp forzado: ε 0→0.5, cruces 0→9/10 |
| **No-monótona** (oscilante) | SDDF grilla | error oscila con N | 07_convergencia_grilla.csv |

**La pregunta abierta:** ¿qué determina el tipo? Hipótesis: el tipo depende
de si el observador es **lineal en el sustrato** (puntual: la inversa es
una operación algebraica) o **estadístico** (gradual: el forzado acumula).
Formalización pendiente.

## 6. El punto irreducible (la respuesta filosófica)

Como la longitud de onda es irreducible al color, **el balance del
presupuesto dual es irreducible al colapso**:

- La longitud de onda existe sin ojo; el color depende del observador.
- El drift -2 existe sin medición; el colapso depende del instrumento.

**La conjetura de Collatz en este marco:** la divergencia requeriría una
medida invariante singular (no-equidistribuida) con soporte en una órbita
infinita. El sustrato (balance -2) no la produce; ningún observador ni
instrumento la produce. **Eso no es una prueba — es la localización exacta
del hueco:** el problema abierto se reduce a la existencia de esa medida.

## 7. Qué falta (matemática nueva posible)

1. **LEH por-órbita**: el puente ensemble→órbita. Posible ataque: mostrar
   que la desviación de equidistribución decae con la longitud de órbita
   (nuestros datos: f_P máx 0.369 en órbitas de ~40 pasos; medir la
   desviación vs longitud para 10⁶ órbitas).
2. **Tipo de transición**: formalizar por qué VSA es puntual y Collatz es
   gradual.
3. **Medidas invariantes singulares**: la existencia de la medida "mala"
   es el enunciado exacto de la conjetura en términos de teoría ergódica.

*Per aspera, ad astra.*
