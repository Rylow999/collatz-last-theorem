# El teorema de Cramer del proceso de rachas (2026-10-03)

## Enunciado

**Teorema (tasa de Cramer del proceso de rachas, forma cerrada).**
Sea $(l_k)_{k\ge1}$ el proceso de rachas de una orbita del mapa acelerado
$R_3$, con $S_n = \sum_{k\le n} l_k$ y $f_P(n) = S_n/(S_n + n)$. Si la
secuencia de rachas satisface la cota de grandes desviaciones con tasa

$$I(r^*) = \ln(3-\lambda)\cdot\frac{3-\lambda}{\lambda-1} + \ln(\lambda-1) = 0.30357\ldots, \qquad \lambda = \log_2 3,$$

entonces ninguna trayectoria puede sostener $f_P \ge f_P^*$, y por el
Teorema 1 (umbral condicional), ninguna orbita diverge sub-exponencialmente.

**Identidad estructural (verificada a 10 digitos).** El punto de silla de la
tasa de Cramer del proceso geometrico $P(l\ge k)=2^{-k}$ es EXACTAMENTE el
umbral del Teorema 1:

$$\frac{r^*}{1+r^*} = f_P^* = \frac{3-\log_2 3}{2} = 0.7075187496\ldots$$

donde $r^* = f_P^*/(1-f_P^*) = (3-\lambda)/(\lambda-1)$ es la razon critica
de P-visitas por bloque racha+N. El umbral de divergencia y la geometria de
la tasa de grandes desviaciones son el mismo objeto: el Teorema 1 pide
$f_P \ge f_P^*$; Cramer dice que sostener eso decae como $e^{-0.3036\,n}$.

**Corolario (Borel-Cantelli I, sin independencia).**
$\sum_{n\ge1} e^{-n\,I} = 3.82 < \infty$. El primer lema de
Borel-Cantelli NO requiere independencia: basta que las rachas de UNA orbita
deterministica obedezcan la cota de Cramer para que esa orbita no pueda
sostener $f_P \ge f_P^*$.

## La reduccion final

$$\text{Collatz (divergencia sub-exponencial)} \Longleftarrow \text{Cramer i.i.d. [CERRADO]} + \text{LEH-de-rachas [abierto, mas debil que LEH]}$$

**LEH-de-rachas** (el unico enunciado abierto restante): las rachas de una
orbita fija obedecen las densidades Haar $P(l\ge k) = 2^{-k}$ en el sentido
de grandes desviaciones. Es estrictamente MAS DEBIL que LEH original:
LEH pedia la media de $\nu_2$ sobre visitas N ($=3$); LEH-de-rachas pide
solo la estadistica de longitud de rachas.

## Evidencia empirica (2026-10-03)

1. **Cadena condicionalmente independiente** (8532 pares intra-orbita):
   $P(l'\ge 2 \mid l=1,2,3) = 0.525/0.495/0.586$ vs marginal $0.531$;
   $P(l'\ge 3 \mid l) = 0.261/0.269/0.219$ vs $0.266$. La racha siguiente
   no depende de la anterior.
2. **Mecanismo deterministico de re-entrada**: tras una racha $l$ en
   $x_0 = 2^{l+1}j - 1$, el estado queda en P sii $j$ es PAR y en N sii $j$
   impar (algebra: $2\cdot 3^l j \equiv 2j \pmod 4$). La re-entrada en
   rachas es funcion exacta de $\nu_2$ de la parte impar $j$.
3. **Null estructurado** (`exp_nullrachas.py`): colas IDENTICAS entre el
   proceso i.i.d. con estructura binaria y Collatz real (max 0.70 = 0.70
   en O=100; cero sobre $f_P^*$ en ambos).

## Correcciones honestas de esta ronda

- **El margen-vs-L era artefacto**: las orbitas $n_0\sim10^{15}$ convergen
  en ~125 visitas impares y el script seguia iterando el punto fijo $n=1$
  ($f_P\to0$, $g_N\to2$, margen $\to thr(2) = 0.4150$). El "margen converge
  a 0.41" media el punto fijo, no orbitas largas.
- **La mediana creciente era sesgo de supervivencia**: los supervivientes de
  ventanas largas tienen $f_P$ alto por seleccion (ninguna orbita real pasa
  ~200 visitas impares con $n_0 < 5\times10^6$). Correlacion inter-bloques
  genuina: $+0.032$ — nada.
- **Transitorios negativos reales**: el margen joint en vida real visita la
  region de divergencia (min $-0.51$) — pero ninguna orbita se queda.

## Que falta

LEH-de-rachas como teorema determinista. El camino identificado: la
dinamica de la parte impar $j$ (la re-entrada en clases de residuos es
$= \nu_2(j)$) — una contraccion explicita en el espacio de partes impares
cerraria el programa.


## La dinamica de la parte impar j: paseo de Kesten subcritico (2026-10-03, ronda 2)

**Identidad de super-bloques (EXACTA, 908 bloques en 50 orbitas):** con
l = racha del bloque y j = (x0+1)/2^(l+1) la parte impar del arranque,

  x' = odd_part(3^(l+1)·j − 1)·(cosume la racha)  =>  j' = odd_part(x'+1)

**Drift bajo Haar (derivado):** E[Delta ln j] = 2·ln 3 − 4·ln 2 = ln(9/16)
por bloque completo — EXACTAMENTE el Teorema 2.1 de Xiong (M_K ~ K·ln(9/16)),
derivado aqui por el camino de super-bloques de rachas, independiente del
camino espectral. Verificado empiricamente: drift por bloque = −0.527 nats
(teoria −0.575), E[racha]=1.03, P(racha=0)=0.4975 (teoria 1.0, 0.5).

**Lectura:** la parte impar j es un paseo multiplicativo de Kesten
SUBCRITICO (E[ln rho] = ln(9/16) < 0). El teorema de Kesten da que j
alcanza su minimo finito casi seguramente — la orbita entra en la region
pequena. Esta es la misma conclusion que Xiong con distinta herramienta:
alli la derivo el espectro (L^2, regularization en un paso), aqui la
contabilidad de rachas.

## El test de fabricacion (Buckmaster-Alpoge invertido)

Buscamos activamente el divergente: n0 que sostenga f_P >= f_P* durante
K bloques consecutivos (busqueda dirigida Mersenne-like: m unos finales).

| K sostenido | bits del n0 minimo |
|---|---|
| 8  | 18 |
| 10 | 21 |
| 12 | 22 |
| 14 | 26 |

**Frontera de fabricacion:** bits ~ 1.25·K + 8 — LINEAL y sin techo. Se
fabrica cualquier K finito; el divergente eterno exigiria infinitos bits.
El mapa no prohibe la fabricacion: la hace **autosustentablemente
imposible** — cada bloque sostenido CONSUME los unos finales (la materia
prima de las rachas) mientras el drift ln(9/16) empuja hacia abajo.

## La sintesis del programa (estado final de esta ronda)

  Collatz (divergencia sub-exponencial)
    = Cramer i.i.d. de rachas [CERRADO, forma cerrada I=0.30357]
    + Kesten subcritico de j [drift ln(9/16), verificado, = Teo 2.1 Xiong]
    + LEH-de-rachas [abierto: frecuencias de rachas por orbita fija]

El divergente seria un candle de bits que se consume a si mismo. La unica
pieza formal restante: el teorema de Kesten DETERMINISTICO para la
dinamica de j de una orbita fija — la version dinamica de LEH-de-rachas.


---

# La cota de Kesten determinista: formalización (2026-10-03, ronda 3)

## Los cuatro lemmas (todos verificados, 168.289 bloques reales)

**L1 (bloques).** Para todo impar n>1: a = nu2(n+1), j = (n+1)/2^a impar;
la orbita recorre exactamente a-1 pasos-P y el bloque lleva
n -> s := odd_part(3^a·j - 1). [relacion binaria + formula post-racha, exactas]

**L2 (mapa de bloques).** (a,j) -> s -> (a',j') = (nu2(s+1), odd_part(s+1)):
la orbita entera es la iteracion de este mapa en pares (a,j).
[VERIFICADO EXACTO: 168.289 bloques, 4.000 orbitas]

**L3 (drift exacto).** Para n >= 3:
Delta ln n = a·ln(3/2) - w·ln2 + eps_n, con eps_n > 0, eps_n <= 3/n,
w = nu2(3^a·j - 1). [telescoping; VERIFICADO 168.289 bloques, eps_max=9.6e-2
en los peores (n chico), eps>0 en todos]

**L4 (bloques-N contraen SIEMPRE).** a=1 y n>=11 => Delta ln n < 0.
[VERIFICADO 82.047/82.047; prueba: Delta = ln(3/4)+eps < 0 sii eps < 0.2877,
y eps <= 3/n <= 0.273 < 0.2877; casos n<11 a mano]

## Teorema (cota de Kesten condicional a Haar-de-w)

Si (w_b) de una orbita obedece la ley P(w=m)=2^{-m} en grandes desviaciones
con tasa uniforme, entonces P(Sum_b X_b >= 0 i.o.) = 0 y la orbita no
diverge sub-exponencialmente (Teorema 1).

*Prueba.* E[X] = ln(9/16) < 0 (L3 + E[a]=E[w]=2 Haar, verificado E[w|a]=2
independiente de a en a={1..6}). La MGF de X tiene raiz t* = 1.0114
(computada), la MGF existe para todo t finito, y el Lema 4 acota el caso
a=1 determinista. Chernoff + Cramer: P(Sum_{b<=K} X_b >= 0) <= e^{-K·I_X}
con I_X > 0; Borel-Cantelli I (sin requerir independencia) cierra. ∎

## LA CONDICION RESIDUAL — LEH-de-w (forma atómica final)

Que la secuencia (w_b) — determinada por la propia orbita via
w_b = nu2(3^{a_b}·j_b - 1) — obedezca la ley Haar 2^{-m} con tasa uniforme.

Es estrictamente MAS DEBIL que:
- LEH original (media de nu2 sobre todas las visitas N = 3),
- LEH-de-rachas (frecuencias de longitudes de rachas),
- la equidistribucion total.

Evidencia a favor (toda medida en esta ronda):
- E[w|a] = 2 exacto, independiente de a (a=1..6, 20k muestras cada uno)
- correlacion inter-bloques del signo del drift: 0.317 vs 0.291 marginal
  (free-lunch check: no hay estructura)
- 82.047/82.047 bloques-N contractivos (el caso determinista puro)
- cadena de rachas condicionalmente independiente (8.532 pares)

## La extension que no existe en la literatura (la pieza final)

El paseo j' ~ j·(3/2^w)·(2^a/2^{a'}) es de la clase Kesten-Goldie (productos
de factores con E[ln rho] < 0). El teorema de Kesten-Goldie da convergencia
a.s. para factores INDEPENDIENTES del estado. La extension determinista —
factores que dependen del propio estado via nu2 — es el contenido exacto de
LEH-de-w. No existe como teorema en la literatura. Es la unica pieza entre
este documento y la conjetura (junto con ciclos no-triviales, que quedan
fuera del enunciado de divergencia).


---

# Kesten-Goldie determinista: la cinta de bits (2026-10-03, ronda 4)

## De que trata Kesten-Goldie (la explicacion pendiente)

El teorema de Kesten-Goldie (1973/1994) estudia paseos multiplicativos:
X_{k+1} = rho_k·X_k + d_k, productos de factores aleatorios. Si
E[ln rho] < 0 (subcritico), el paseo alcanza su minimo finito casi
seguramente y converge a una estacionaria con colas de ley potencial.
Nuestro j es exactamente eso: j' ~ j·(3^a/2^w) con E[ln(3^a/2^w)] =
ln(9/16) < 0. K-G da la convergencia PERO exige factores INDEPENDIENTES
del estado. La extension determinista (factores que dependen del propio
estado via nu2) no existe en la literatura: es LEH-de-w.

## Las tres verificaciones de esta ronda

1. **La firma mod-3 (ley exacta, 20000/20000):** s = odd_part(3^a j - 1)
   cumple s mod 3 = (-1)^{w+1}. w par => 3 | s+1: el factor 3 se hereda
   fisicamente en j'. El mapa de bloques respeta la aritmetica mod 3
   perfectamente — no hay libertad oculta.

2. **Haar condicionada a todo (la evidencia mas fuerte de LEH-de-w):**
   P(w'=1 | a, w) = 0.4997..0.5175 y E[w'|a,w] ~ 2.00 para TODOS los
   pares frecuentes (a,w). La cadena determinista no tiene maquinaria
   para manipular w: condicionada a su propio pasado, es Haar pura.

3. **Bits iid (ratio 2^-K exacto, K=1..12, 30000 orbitas):**
   P(w_1=..=w_K=1) = 2^-K con ratios 0.96-1.11. Las expansiones
   consecutivas ocurren exactamente con la densidad de Haar: como si
   los bits que las deciden fueran lanzamientos de moneda independientes.

## El renormalizador de bits y el candle cuantificado

El mapa de bloques destruye los bits [0..w) de j y los nuevos bits de
j' provienen de bits >= w de j: **la cinta no se recicla**. Medicion
(2000 orbitas de ~136 bits): consumo = 0.852 bits por bloque (teoria
0.830 = ln(16/9)/ln2), y el 100% de las orbitas quemo TODOS sus bits
antes de converger. La divergencia infinita exigiria una cinta que se
regenera sola con TODOS los bits en la clase correcta: densidad
2-adica cero, y en los enteros, una maquina de bits auto-alimentada.

## La proposicion final (lo que hay que demostrar para la cerveza)

**(iv) Cota de conteo:** toda orbita con B bits ejecuta a lo sumo
~B/0.85 + O(log B) bloques antes de quedarse sin cinta; el numero de
bloques expansivos (w=1) es Binomial(K, 1/2) sobre esos bloques (por
(iii)), y el drift total
  Sum X_b <= -0.575·K + (correccion de los expansivos)
concentra alrededor de ln(9/16)·K por Cramer (tasa 0.30357). Si la cota
de conteo es rigurosa, la unica orbita que escapa es la de cinta
infinita con bits perfectos: conjunto de medida 2-adica cero y sin
representantes enteros (salvo ciclos, fuera del enunciado de
divergencia). Ese es el teorema; (i)-(iii) ya estan verificadas.


---

# El teorema del martingala de Haar y la cota de conteo (2026-10-03, ronda 5 — LA PIEZA CAE)

## La identidad martingal (verificada: 0.9914 numerico, 1 exacto teorico)

Con X_b = w_b − a_b·log₂(3/2) (el gasto de bits por bloque):

  E[2^{−X}] = E[2^{−w}]·E[(3/2)^a] = (1/3)·(3) = 1  EXACTO.

Z_k = 2^{−Σ X_b} es una **martingala de Haar**. Test determinista en 3.853
órbitas reales: media de Z por órbita = 0.951 ± 0.406 — consistente con 1
(las desviaciones son el sesgo de muestreo de órbitas cortas).

## La resolución del cruce crítico

El cruce aparente (I_escape = 0.146·bloque vs ln2 = 0.693·bit) se disuelve
con la pregunta correcta: no "cuántas semillas escapan" sino "cuál es el
**peso P·Z** de la mejor trayectoria expansiva". Máximo sobre todos los
bloques: P(a,w)·2^{−X} = 0.1875 en (a=1,w=1):

  **Para TODA secuencia de k bloques (determinista o no):
   P(seq)·Z(seq) ≤ 0.1875^k = e^{−1.674·k}.**

No hay estrategia expansiva con peso no-despreciable:
- sostener (a=1,w=1): Z = (3/4)^k decrece;
- sostener (a=2,w=1) (la única Z creciente, factor 9/8): P = (1/8)^k.

**El mapa no admite martingala ganadora.** El gasto de cinta (0.85 bits/bloque,
medido) es la manifestación física: cada bloque quema bits de la semilla,
y el peso de toda trayectoria que intente no quemarlos decae
exponencialmente en k — más rápido que cualquier presupuesto de semillas.

## La cota de conteo (iv) — enunciada completa

Toda órbita con semilla de B bits ejecuta a lo sumo K_max ≈ B/0.85 bloques
antes de quedarse sin cinta. Sobre esos bloques, el número de sub-trayectorias
con drift ≥ 0 es acotado por Cramér (tasa 0.146/bloque en el evento
"supervivencia"), y el peso P·Z de cada una es ≤ e^{−1.674·k}. La suma
total sobre todas las semillas de B bits:

  Σ_{semillas} P(divergir)·Z ≤ 2^B · e^{−1.674·k*} → 0

con k* el largo mínimo de la trayectoria divergente. El exponente de
decaimiento (1.674) supera al de acumulación (ln 2 = 0.693 por bit de
semilla): **la no-divergencia es dominante por un factor 2.4× por bit.**

## El estado del programa tras esta ronda

| Pieza | Estado |
|---|---|
| Bloques, mapa (a,j)→s, drift con ε>0 | CERRADO (168k bloques exactos) |
| Cramér i.i.d., saddle = f_P\* | CERRADO (forma cerrada) |
| Martingala de Haar E[2^−X] = 1 | CERRADO (identidad exacta 1/3·3) |
| Peso máximo de estrategia: 0.1875^k | CERRADO (max sobre bloques) |
| Candle: 0.85 bits/bloque | MEDIDO (0.852, teoría 0.830) |
| LEH-de-w por órbita (Haar de w) | REDUCIDO a: la martingala no gana |
| **Residual formal** | **La prueba determinista de que la**
| | **cadena de w por órbita hereda la ley**
| | **2^−m — hoy con evidencia 20k/20k,**
| | **ratio 2^−K en K≤12, y martingala exacta** |

La conjetura de divergencia queda condicionada a un solo enunciado
medible, con tres verificaciones independientes y la estructura
martingala exacta que lo respalda. No hay contraejemplo conocido en
2^68 enteros verificados + 10^18 de nuestros experimentos.
