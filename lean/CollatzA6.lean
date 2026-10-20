import Mathlib.Tactic

/-!
# Collatz A6 (Lean 4) — v19: SORRIES CERRADOS con Mathlib v4.34.1

CERRADOS SIN SORRY (nucleo de A6 + mecanica Nat.pow/mod):
  v2, v2_impar_cero, v2_par_pos, v2_uno (ambos sentidos),
  pasoP_iff (iff base de la relacion binaria), pasoP_algebra,
  cuatro_div_pot (4 | 2^k para k >= 2),
  pot_por_j_mod4 (4 | 2^(k+1)*j para k >= 1),
  rachaF_eq_k (racha desde 2^(k+1)*j - 1 con j impar = exactamente k).

CORRECCION HONESTA (Metodo Integral, etiquetado):
  El enunciado declarado en v16 como `rachaF_ge`
  (`rachaF fuel (2^(k+1)*j - 1) >= k + 1` para j impar) era FALSO por
  off-by-one: verificacion numerica (k < 8, multiples j impares) muestra
  que la racha es EXACTAMENTE k. Se prueba abajo como `rachaF_eq_k`.
  Tecnica: unfold de rachaF punto a punto (con fuel literal f+1 tras
  `cases fuel`; `simp only [rachaF]` no reduce con fuel variable) y
  unfold de v2 en forma-sucesor (x = (2*X-1)+1).
-/

def v2 : Nat → Nat
  | 0 => 0
  | n+1 => if (n+1) % 2 = 0 then v2 ((n+1)/2) + 1 else 0

theorem v2_impar_cero (m : Nat) (h : m % 2 = 1) : v2 m = 0 := by
  match m with
  | 0 => omega
  | k+1 => unfold v2; rw [if_neg (by omega : (k+1) % 2 ≠ 0)]

theorem v2_par_pos (m : Nat) (h : m % 2 = 0) (hpos : m > 0) : v2 m >= 1 := by
  match m with
  | 0 => omega
  | k+1 => unfold v2; rw [if_pos (by omega : (k+1) % 2 = 0)]; omega

theorem v2_uno_de_tres_mod_cuatro (n : Nat) (h : n % 4 = 3) :
    v2 (3*n+1) = 1 := by
  have hpar : (3*n+1) % 2 = 0 := by omega
  have hm : ((3*n+1)/2) % 2 = 1 := by omega
  have key : 3*n+1 = (3*n)+1 := rfl
  rw [key] at hpar hm ⊢
  unfold v2
  rw [if_pos (by omega : (3*n+1) % 2 = 0)]
  rw [v2_impar_cero _ hm]

theorem v2_uno_implica_P (n : Nat) (hn : n % 2 = 1) (h : v2 (3*n+1) = 1) :
    n % 4 = 3 := by
  by_cases h4 : n % 4 = 3
  · exact h4
  · exfalso
    have h1 : n % 4 = 1 := by omega
    have hpar2 : ((3*n+1)/2) % 2 = 0 := by omega
    have hpos2 : (3*n+1)/2 > 0 := by omega
    have hv : v2 (3*n+1) >= 2 := by
      rw [show 3*n+1 = (3*n)+1 from rfl]
      unfold v2
      rw [if_pos (by omega : (3*n+1) % 2 = 0)]
      have := v2_par_pos ((3*n+1)/2) hpar2 hpos2
      omega
    omega

theorem pasoP_iff (n : Nat) (hn : n % 2 = 1) :
    n % 4 = 3 ↔ v2 (3*n+1) = 1 :=
  ⟨fun h => v2_uno_de_tres_mod_cuatro n h, v2_uno_implica_P n hn⟩

theorem pasoP_algebra (m : Nat) (hm : m % 2 = 1) :
    (3*(2*m-1)+1)/2 = 3*m - 1 := by omega

def rachaF : Nat → Nat → Nat
  | 0, _ => 0
  | f+1, n =>
    if n > 1 ∧ n % 4 = 3 ∧ v2 (3*n+1) = 1
    then rachaF f ((3*n+1)/2) + 1
    else 0

/-- 4 | 2^k para k >= 2. -/
theorem cuatro_div_pot : forall k : Nat, k >= 2 → (2^k) % 4 = 0 := by
  intro k hk
  induction k with
  | zero => omega
  | succ n ih =>
    if h2 : n >= 2 then
      have hpow : 2^(n+1) = 2^n * 2 := Nat.pow_succ 2 n
      have hdvd : (4 : Nat) ∣ 2^n := Nat.dvd_iff_mod_eq_zero.mpr (ih (by omega))
      have h2d : (4 : Nat) ∣ 2^n * 2 := Nat.dvd_mul_of_dvd_left hdvd 2
      rw [hpow]
      exact Nat.dvd_iff_mod_eq_zero.mp h2d
    else
      have hn01 : n = 0 ∨ n = 1 := by omega
      rcases hn01 with rfl | rfl
      · omega
      · norm_num [Nat.pow_succ]

/-- (2^(k+1)*j) % 4 = 0 para k >= 1. -/
theorem pot_por_j_mod4 (k j : Nat) (hk : k >= 1) :
    (2^(k+1) * j) % 4 = 0 := by
  have h : (2^(k+1)) % 4 = 0 := cuatro_div_pot (k+1) (by omega)
  have hdvd : (4 : Nat) ∣ 2^(k+1) := Nat.dvd_iff_mod_eq_zero.mpr h
  exact Nat.dvd_iff_mod_eq_zero.mp (hdvd.mul_right j)

/-- [CORREGIDO y PROBADO] Racha de P-steps desde 2^(k+1)*j - 1 con j impar:
    es EXACTAMENTE k. (El enunciado anterior >= k+1 era falso.) -/
theorem rachaF_eq_k (k j fuel : Nat) (hj : j % 2 = 1) (hfuel : k <= fuel) :
    rachaF fuel (2^(k+1)*j - 1) = k := by
  induction k generalizing j fuel with
  | zero =>
    have hn4 : (2*j - 1) % 4 = 1 := by
      obtain ⟨t, ht⟩ : ∃ t, j = 2*t + 1 := ⟨j / 2, by omega⟩
      subst ht
      omega
    cases fuel with
    | zero => rfl
    | succ f =>
      simp only [rachaF]
      rw [if_neg (by omega)]
  | succ k ih =>
    -- cotas de los atomos de potencia (omega no las conoce)
    have hpk : 2^k >= 1 := by
      induction k with
      | zero => norm_num
      | succ m ihm =>
        have hps : 2^(m+1) = 2^m * 2 := Nat.pow_succ 2 m
        rw [hps]; omega
    have h2k1 : 2^(k+1) = 2^k * 2 := Nat.pow_succ 2 k
    have ha : 2^(k+1) >= 2 := by rw [h2k1]; omega
    have h2k2 : 2^(k+2) = 2^(k+1) * 2 := Nat.pow_succ 2 (k+1)
    have ha4 : 2^(k+2) >= 4 := by rw [h2k2]; omega
    have hp : 2^(k+2) = 2^(k+1) * 2 := Nat.pow_succ 2 (k+1)
    have hnpos : 2^(k+2)*j - 1 > 1 := by omega
    have hmod4 : (2^(k+2)*j) % 4 = 0 := pot_por_j_mod4 (k+1) j (by omega)
    have hn4 : (2^(k+2)*j - 1) % 4 = 3 := by omega
    have h2dvd : (2 : Nat) ∣ 3 * 2^(k+1) * j := by
      refine ⟨3 * 2^k * j, ?_⟩
      rw [Nat.pow_succ]; ring
    have hm'odd : (3*2^(k+1)*j - 1) % 2 = 1 := by
      have hz := Nat.dvd_iff_mod_eq_zero.mp h2dvd
      omega
    have hv2 : v2 (3*(2^(k+2)*j - 1) + 1) = 1 := by
      have heq : 3*(2^(k+2)*j - 1) + 1 = (2*(3*2^(k+1)*j - 1) - 1) + 1 := by
        rw [hp]; omega
      have hcond : ((2*(3*2^(k+1)*j - 1) - 1) + 1) % 2 = 0 := by omega
      have hdiv2 : ((2*(3*2^(k+1)*j - 1) - 1) + 1) / 2 = 3*2^(k+1)*j - 1 := by omega
      rw [heq]
      unfold v2
      rw [if_pos hcond]
      rw [hdiv2]
      rw [v2_impar_cero _ hm'odd]
      norm_num
    have h3j : (3*j) % 2 = 1 := by omega
    cases fuel with
    | zero => omega
    | succ f =>
      simp only [rachaF]
      rw [if_pos ⟨hnpos, hn4, hv2⟩]
      have hdiv : (3*(2^(k+2)*j - 1) + 1)/2 = 2^(k+1)*(3*j) - 1 := by
        rw [hp]; omega
      rw [hdiv]
      rw [ih (3*j) f h3j (by omega)]
