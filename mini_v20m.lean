import Mathlib.Tactic.Omega
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Data.Nat.Defs

/-!
# Collatz A6 (Lean 4) — v20: SORRIES CERRADOS con Mathlib v4.34.1

CERRADOS SIN SORRY (nucleo de A6 + mecanica Nat.pow/mod):
  v2, v2_impar_cero, v2_par_pos, v2_uno (ambos sentidos),
  pasoP_iff, pasoP_algebra, cuatro_div_pot, pot_por_j_mod4,
  rachaF_eq_k (racha desde 2^(k+1)*j - 1 con j impar = exactamente k).

CORRECCION HONESTA (Metodo Integral): el enunciado v16 `rachaF_ge`
(>= k+1 con j impar) era FALSO por off-by-one; reformulado y probado
como rachaF_eq_k (exactamente k).
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

theorem cuatro_div_pot : forall k : Nat, k >= 2 → (2^k) % 4 = 0 := by
  intro k hk
  induction k with
  | zero => omega
  | succ n ih =>
    if h2 : n >= 2 then
      have hpow : 2^(n+1) = 2^n * 2 := Nat.pow_succ 2 n
      have hdvd : (4 : Nat) ∣ 2^n := Nat.dvd_iff_mod_eq_zero.mpr (ih (by omega))
      have h2d : (4 : Nat) ∣ 2^n * 2 := hdvd.mul_right 2
      rw [hpow]
      exact Nat.dvd_iff_mod_eq_zero.mp h2d
    else
      have hn01 : n = 0 ∨ n = 1 := by omega
      rcases hn01 with rfl | rfl
      · omega
      · norm_num [Nat.pow_succ]

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
    -- cotas de potencias: inducciones locales de enunciado LINEAL
    have hxp : forall m : Nat, 0 < 2^m := by
      intro m
      induction m with
      | zero => norm_num
      | succ t iht =>
        have hps : 2^(t+1) = 2^t * 2 := Nat.pow_succ 2 t
        rw [hps]; omega
    have hxp2 : forall m : Nat, 4 ≤ 2^(m+2) := by
      intro m
      induction m with
      | zero => norm_num
      | succ t iht =>
        have hps : 2^(t+3) = 2^(t+2) * 2 := Nat.pow_succ 2 (t+2)
        rw [hps]; omega
    -- 4 | 2^(k+2)*j (teorema cerrado) → n ≡ 3 (mod 4)
    have hmod4 : (2^(k+2)*j) % 4 = 0 := pot_por_j_mod4 (k+1) j (by omega)
    have hn4 : (2^(k+2)*j - 1) % 4 = 3 := by omega
    -- n > 1: testigo con j = t+1 (todo lineal)
    have hge4 : 4 ≤ 2^(k+2)*j := by
      obtain ⟨t, ht⟩ : ∃ t, j = t + 1 := ⟨j - 1, by omega⟩
      subst ht
      have hpr : 2^(k+2)*(t+1) = 2^(k+2)*t + 2^(k+2) := by ring
      rw [hpr]
      have h1 : 4 ≤ 2^(k+2) := hxp2 k
      omega
    have hnpos : 1 < 2^(k+2)*j - 1 := by omega
    -- v2 (3n+1) = 1: GRatis del teorema ya probado (n ≡ 3 mod 4)
    have hv2 : v2 (3*(2^(k+2)*j - 1) + 1) = 1 :=
      v2_uno_de_tres_mod_cuatro _ hn4
    -- hijo: (3n+1)/2 = 2^(k+1)*(3j) - 1, por testigo exacto + cancel_left
    have h3j : (3*j) % 2 = 1 := by
      obtain ⟨t, ht⟩ : ∃ t, j = 2*t + 1 := ⟨j / 2, by omega⟩
      subst ht
      omega
    cases fuel with
    | zero => omega
    | succ f =>
      simp only [rachaF]
      rw [if_pos ⟨hnpos, hn4, hv2⟩]
      have hdiv : (3*(2^(k+2)*j - 1) + 1)/2 = 2^(k+1)*(3*j) - 1 := by
        have hps : 2^(k+2) = 2^(k+1) * 2 := Nat.pow_succ 2 (k+1)
        have key : 3*(2^(k+2)*j - 1) + 1 = 2*(2^(k+1)*(3*j) - 1) := by
          rw [hps]; ring
        rw [key, Nat.mul_div_cancel_left _ (by omega : (2:Nat) ≠ 0)]
      rw [hdiv]
      rw [ih (3*j) f h3j (by omega)]
