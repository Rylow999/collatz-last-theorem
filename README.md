# Collatz Last Theorem

**Converting the Collatz Conjecture into a corollary of the bound on the equidistribution deviation.**

> **PROGRAM STATE (Integral Method audit, 2026-10-10):**
> proven theorems A1-A8 (sign, deposits, ν₃=0, martingale, Cramér,
> binary relation) · conditional closure to hypothesis [H] (parity core:
> deposit bits ~ currency) · [H] **open**, with strong evidence
> (fabricated 10/10, greedy, automatic) and none against ·
> protocol: `HORIZON/DOCUMENTATION/METODO_INTEGRAL.md` (mandatory state labeling in all future documents).

Author: Luciano Benjamín Nieto · Assistance: Nexus (agent)
License: CC-BY 4.0

---

## The idea in one page

The Collatz Conjecture (every orbit of the 3n+1 map reaches 1) remains open
because no finite verification can close a statement about all integers. But the
LOGOS/COLLATZ program
([`Rylow999/vega-vault`](https://github.com/Rylow999/vega-vault))
derived a **conditional exact threshold**:

$$f_P^* = \log_4(8/3) = 0.7075$$

**Theorem (proven, conditional to LEH):** if an orbit diverges sub-exponentially,
then its frequency of visits to the class P = {n ≡ 3 mod 4} satisfies f_P ≥ f_P*
throughout the orbit.

**This repository seeks the missing step:** demonstrating that this condition
**never holds** — i.e., the **bound**:

$$|f_P - \mu| \leq C \quad \text{for all orbits, with } C < f_P^* - \mu$$

where μ ≈ 0.324 is the empirical mean of f_P (the invariant measure of the map).
If the bound holds with C < 0.374, the conjecture follows as a corollary:
**no orbit can sustain f_P ≥ 0.7075, then no orbit diverges**.

## Why this is attackable

1. **Standard ergodic theory**: bound on the deviation of the invariant measure
   — a statement weaker than LEH (orbitwise equidistribution) and with known tools.
2. **The threshold is exact and already derived** — it does not depend on tuning.
3. **The gap is measurable**: numerical evidence (100k orbits) shows Collatz
   accumulates deviation slower than equivalent random, with short tail
   (0.135%) and no divergent orbits.

## Key numerical findings (exp_theorema.py experiment)

With 100,000 orbits (odd numbers up to 2M) and null model with the same
structure of the map (P=1/3 + geometric clusters of N):

| System | Exponent b (|f_P−ref| ~ n^b) |
|---|---|
| CLT naive (Terras simplified, i.i.d.) | −0.500 |
| **Null (P=1/3 + clusters)** | **−0.472** (the null DOES cancel as CLT predicts) |
| **Collatz vs invariant measure (μ=0.324)** | **−0.264** |
| **GAP** | **+0.21 — Collatz ACCUMULATES more deviation than random** |

**The tail exists**: 135/100,000 orbits (0.135%) with |f_P−1/3|>0.15 —
and **all converge** (no real divergence until n=2M).

**Reading**: the map is not a perfect die — it has "structural memory"
that accumulates deviation more than random. That memory is the **real substrate**
where a divergent orbit would have to live. The theorem to seek is the
**bound** of that memory.

### The bound (`exp_acotacion.py`, 400k orbits up to n₀=5×10⁶)

- **Genuine C* = 0.2036–0.25** — robust to step cap (10³ to 5×10⁵: the
  maximum STABILIZES at 0.2036). The 0.3089 from window sweep included
  trivial orbits with f_P=0 (the n that drop directly).
- **The margin against the threshold is +0.124** (0.374 − 0.25) — more leeway.
- **The null is also bounded** (0.234) but Collatz exceeds it: the excess
  (real substrate) has a ceiling.

### The one-sided bound (`recomputo_onesided.py`, 2026-10-02) — the correct side

**Fundamental correction of the approach:** the symmetric bound |f_P−μ|≤C was the
wrong side of the divergence theorem. The divergence theorem is **one-sided**:
divergent ⟹ f_P **sustained** ≥ f_P*. What must be bounded is the **upper
deviation** C+ = max(f_P−μ), not the symmetric — C* are dominated by trivial
orbits with f_P=0 (C−=0.4725 confirms the diagnosis).

- **C+ = 0.2061 → one-sided margin = +0.0289 OK** (200k orbits, def B: μ=0.4725)
- One-sided windows **all positive**: +0.0016 (0.5M), +0.0233 (1M), +0.0075 (3M), +0.0310 (5M)
- **max f_P = 0.6786 < f_P* = 0.7075** — no orbit approaches the threshold
- The symmetric bound breaks (−0.237): it was the wrong side, not a conjecture problem

**State**: the one-sided bound is numerically upheld throughout the tested range.
The remaining formal step: prove C+ < f_P*−μ — deterministic bound on the upper
deviation (one-sided large deviations: the ATTACK 1 already developed, now
targeted at the correct side).

### ATTACK 1 RE-POINTED (`ataque1_onesided.py`, 2026-10-02) — the verdict

Large deviations **ONE-SIDED** with def B — the original attack tested the
symmetric bound (wrong side, dominated by trivial f_P=0) with def A
(steps, not odd values) and never ran (I_null=None at 10σ).

- **Null (binomial Haar 50/50, exact KL rate):** I(c+) = **0.1148/visit**;
  exact tails by n: 2.1e-2 (n=20), 4.7e-4 (50), 8.3e-7 (100), 1.0e-11 (200);
  **Borel-Cantelli sum (n=10..5000) = 0.0759, finite**.
- **Real Collatz (150k genuine orbits, real lengths):** **0 violations
  one-sided in any window** — L~20: 0/54737, L~50: 0/127713,
  L~100: 0/74187, L~200: 0/4979. Suppression of the upper tail relative to
  Haar: the bias factor μ is **~1.8×** (correction 2026-10-03: the reading
  "≥100×" was partially a length-matching artifact — see below).
- **Verdict**: I(c+) > 0 → Σ P_null(n) converges → **P(orbit with f_P
  sustained > f_P*) = 0 under the model** (Borel-Cantelli). And the old
  table old correction: one-sided (the side that matters), the map's
  memory **suppresses** the upper tail — the "gap +0.21, accumulates more
  deviation" was reading the symmetric side.

**Program state**: the Tao null is bounded and Collatz is MORE bounded
than the null on the side the theorem needs. The remaining formal step:
the deterministic bound C+ < f_P*−μ (rigorous one-sided large deviations —
the KL rate 0.1148/visit is the natural candidate as constant of the exponent,
with cluster placement as correction).

### The RPF series (`recomputo_defB.py` + `rpf_*.json`) — the ergodic operator

The ergodic complement: preimages of the map accelerated by mod 3
(`rpf_transfer_operator.json`: preimage, ν pairs), weights of the transfer
matrix over 2^m states (`rpf_v2_pesos.json`: λ1 ~ 0.29–0.34; m=4
practically deterministic, λ2/λ1 ≈ 0.67 for m≥5), attractor of the operator
(`rpf_v3_atractor.json`), and m=11/12 (`rpf_v3_m11_12.json`: N=683/1365, gap
0.069/0.034 — decays ~2^−m: consistent with geometric mixing). Working
hypothesis: the transfer operator gap is the mixing bound ATTACK 3 (ergodicity,
rate 0.054) needs for the deterministic step.

### THE REMAINING STEP: generalized theorem without LEH (`exp_teorema_generalizado.py`, 2026-10-02)

**The generalization that closes the conceptual gap:** the 1 threshold paper
fixes ḡ_N = 3 (Haar ensemble) — that requires LEH (local equidistribution,
not proven). But the algebra of telescoping leaves the
**generalized per-orbit threshold**, conditional SOLELY on the telescoping:

$$f_P \geq \mathrm{thr}(\bar g_N) = \frac{\log_2 3 - \bar g_N}{1 - \bar g_N}$$

with ḡ_N the mean of ν₂(3n+1) **executed by the orbit itself** (over its
visits to N). With ḡ_N = 3 we recover f_P* = 0.7075187496 **exact** (check at
10⁻¹²). The drift identity per segment is verified in 3000 orbits
(residue = the correction (3n+1)/n vs 3n, dominated by the tiny tail — O(1),
not error).

**Result (150k genuine orbits):**

| quantity | value |
|---|---|
| **minimum joint thr(ḡ_N) − f_P:** | **+0.0571** (positive in ALL orbits) |
| median of the margin | +0.2116 |
| orbits in divergence region | **0 of 150000** |
| simple version (ḡ_N ≥ 3 fixed) | **false per orbit** (24924 violations: ḡ_N fluctuates 2.41–18) |

**Reading (so far)**: every orbit either has f_P low or ḡ_N high — the
compensation joint thr(ḡ_N)−f_P > 0 is never violated. The divergence threshold
remains conditional **only on the telescoping** (arithmetic identity), without
equidistribution: LEH is replaced by the realized mean of the orbit itself.
What remains formal: enunciate the identity as lemma (it's direct algebra of
the telescoping with the documented correction) and the margin as observation —
the global deterministic bound C+ remains the open step (the thr(ḡ_N) curve
explains WHY the one-sided margin is stable: orbits with high f_P have high
ḡ_N that compensates).

### Formalization in Lean 4 (A6, `lean/CollatzA6.lean`) — 9 theorems without sorry

The binary relation of streaks is formalized in Lean 4 (v4.34.1 toolchain
with Mathlib). State v24 (2026-10-20; verified build on the Arch workstation: 3093 jobs, EXIT 0, 0 sorry):

- **Core (no sorry):** `v2` (def), `v2_impar_cero`, `v2_par_pos`,
  `v2_uno` in both directions, `pasoP_iff` (the complete iff: n odd with
  n = 3 mod 4 iff v2(3n+1) = 1), `pasoP_algebra`.
- **Mechanized Nat.pow/mod (closed with Mathlib):** `cuatro_div_pot`
  (4 | 2^k for k ≥ 2), `pot_por_j_mod4` (4 | 2^(k+1)·j for k ≥ 1).
- **Honest correction (Integral Method):** the statement declared in v16
  (`rachaF fuel (2^(k+1)*j - 1) ≥ k+1` with j odd) was FALSE by
  off-by-one: numerical verification (k<8, multiple j) shows that the streak
  is EXACTLY k. The theorem was reformulated as `rachaF_eq_k`
  (streak = exact k, j odd) and PROVEN without sorry. The j even case
  (streak = k+1) is labeled as pending formalization.

Reproduce:

```bash
cd lean  # with lakefile.toml (mathlib v4.34.1) and lean-toolchain v4.34.1
lake update && lake exe cache get && lake build
```

## Repository structure

```
collatz-last-theorem/
├── README.md            this file (the full program)
├── docs/
│   ├── ESTRATEGIA.md      the full path: LEH → bound → corollary
│   └── umbral_condicional/
│       ├── README.md
│       ├── paper/collatz_divergence_threshold.tex
│       ├── code/collatz_simulation.py
│       └── data/collatz_orbits_50000.csv
├── src/
│   ├── collatz_core.py          the map, orbits, stats
│   ├── exp_theorema.py          numerical evidence (exponent + tail)
│   ├── exp_acotacion.py         search for ceiling C of deviation
│   ├── exp_acotacion_definitiva.py  the genuine ceiling (decays with n0)
│   └── exp_null_model.py        random with same map structure
├── data/            results (JSON/CSV)
├── paper/
│   ├── collatz_last_theorem.tex  the paper (LaTeX)
│   └── references.bib
└── figures/         figures

**Note**: The two repositories (Divergence Threshold + Last Theorem) are
unified under this repo. The step 1 is conserved in
`docs/umbral_condicional/` with its original history.

## The three steps of the program

| Step | What | Status |
|---|---|---|
| 1. Conditional threshold | f_P* = 0.7075 derived (cond. LEH) | DONE proven (LOGOS/COLLATZ repo) |
| 2. Numerical evidence | deviation accumulates over random (+0.21), tail 0.135% that converges | DONE this repo |
| 3. The bound | f_P−μ one-sided ≤ C+ < f_P*−μ (empirical C+ 0.206, margin +0.029) | [OPEN] **the theorem to find** — nucleus A6 formalized in Lean 4 (v24: 9 theorems without sorry) |

If step 3 is proven → **the conjecture is a corollary**.

## Related repositories

- [`Rylow999/vega-vault/LOGOS/COLLATZ`](https://github.com/Rylow999/vega-vault) — the conditional threshold (step 1)
- [`Rylow999/rho-law`](https://github.com/Rylow999/rho-law) — the unifying framework (three layers)
- [`Rylow999/fhrr-rho-collapse`](https://github.com/Rylow999/fhrr-rho-collapse) — the ρ law in VSA
- [`Rylow999/sddf`](https://github.com/Rylow999/sddf) — turbulence (Navier-Stokes)

## Falsifiability

The program is falsable in both directions:
- If an orbit appears with f_P ≥ 0.7075 sustained → counterexample (conjecture false)
- If the bound breaks (exists C > 0.374 needed) → the path closed
- If the bound is proven → **conjecture as corollary**

## Motto

*Per Aspera, Ad Astra.*
