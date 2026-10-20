import Mathlib.Tactic.Omega
theorem t1 (a b : Nat) (h : a ≤ b) : a + 0 ≤ b := by omega
