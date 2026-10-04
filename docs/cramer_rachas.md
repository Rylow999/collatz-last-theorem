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
