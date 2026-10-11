/-!
# Collatz A6 (Lean 4): rachas = unos finales del binario.
CERRADO SIN SORRY: v2, caso-P, iff-base, algebra del paso.
SORRY DECLARADO (1): induccion general con fuel.
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

/-- A6-base [CERRADO SIN SORRY] -/
theorem pasoP_iff (n : Nat) (hn : n % 2 = 1) :
    n % 4 = 3 ↔ v2 (3*n+1) = 1 :=
  ⟨fun h => v2_uno_de_tres_mod_cuatro n h, v2_uno_implica_P n hn⟩

/-- Algebra del paso P [CERRADO] -/
theorem pasoP_algebra (m : Nat) (hm : m % 2 = 1) :
    (3*(2*m-1)+1)/2 = 3*m - 1 := by omega

/-- Racha con fuel. -/
def rachaF : Nat → Nat → Nat
  | 0, _ => 0
  | f+1, n =>
    if n > 1 ∧ n % 4 = 3 ∧ v2 (3*n+1) = 1
    then rachaF f ((3*n+1)/2) + 1
    else 0

/-- Induccion general [SORRY DECLARADO: mecanica del fuel, proxima ronda]. -/
theorem rachaF_ge (k j fuel : Nat)
    (hj : j % 2 = 1) (hj3 : j % 4 = 3) (hfuel : k + 1 <= fuel) :
    rachaF fuel (2^(k+1)*j - 1) >= k + 1 := by
  sorry
