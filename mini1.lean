import Mathlib.Tactic

theorem cuatro_div_pot : forall k : Nat, k >= 2 → (2^k) % 4 = 0 := by
  intro k hk
  induction k with
  | zero => omega
  | succ n ih =>
    if h2 : n >= 2 then
      have hpow : 2^(n+1) = 2^n * 2 := Nat.pow_succ 2 n
      have hdvd : (4 : Nat) ∣ 2^n := Nat.dvd_iff_mod_eq_zero.mpr (ih (by omega))
      have h2d : (4 : Nat) ∣ 2^n * 2 := ⟨2, by omega⟩
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
