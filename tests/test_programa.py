#!/usr/bin/env python3
# test_programa.py — suite de verificacion del programa Collatz (10-10-26)
# Verifica que los JSON de data/ contengan exactamente los numeros que el
# README declara. Corre: python3 tests/test_programa.py
import json
from pathlib import Path

D = Path(__file__).parent.parent / "data"

def load(name):
    return json.loads((D / name).read_text())

def test_teorema_generalizado():
    d = load("teorema_generalizado.json")
    assert d["check_leh_exacto"] is True, "check LEH fallo"
    assert abs(d["margen_min"] - 0.0571) < 0.0001, f"margen_min {d['margen_min']}"
    assert d["violaciones_joint"] == 0, "violaciones joint != 0"
    assert abs(d["f_P_star"] - 0.7075187496) < 1e-9, "f_P* impreciso"

def test_relacion_binaria():
    d = load("relacion_binaria.json")
    assert d["relacion_exacta"] is True
    dens = d["densidad_rachas"]
    for k in ["1", "2", "3"]:
        assert abs(dens[k]["ratio"] - 1.0) < 0.03, f"ratio k={k}: {dens[k]['ratio']}"
    assert abs(d["memoria_racha_v"]["spearman"] - (-0.027)) < 0.005

def test_ataque1_onesided():
    d = load("ataque1_onesided.json")
    assert abs(d["I_kl"] - 0.1148) < 0.0005, f"I_kl {d['I_kl']}"
    assert abs(d["sum_BC"] - 0.0759) < 0.005, f"sum_BC {d['sum_BC']}"
    assert d["n_orbits"] == 150000

def test_recomputo_onesided():
    d = load("recomputo_onesided.json")
    assert abs(d["C_plus"] - 0.2061) < 0.001
    assert abs(d["margen_one_sided"] - 0.0289) < 0.001

def test_nullrachas():
    d = load("nullrachas.json")
    rows = {r["O"]: r for r in d["rows"]}
    r100 = rows[100]
    assert abs(r100["null_max"] - 0.70) < 0.001, f"null_max O=100: {r100['null_max']}"
    assert abs(r100["collatz_max"] - 0.70) < 0.001
    assert r100["collatz_gt_fpstar"] == 0.0
    assert r100["null_gt_fpstar"] == 0.0

def test_margen_vs_L():
    d = load("margen_vs_L.json")
    # NOTA (auditoria 10-10-26): los margenes en L grande midieron el punto
    # fijo n=1 (artefacto documentado en cramer_rachas.md ronda 5/6);
    # el JSON se conserva como registro historico del hallazgo del artefacto.
    cp = {c["L"]: c for c in d["checkpoints"]}
    assert cp[500]["violaciones"] == 0
    assert cp[20000]["violaciones"] == 0

if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    ok = 0
    for fn in fns:
        try:
            fn()
            print(f"  PASS {fn.__name__}")
            ok += 1
        except AssertionError as e:
            print(f"  FAIL {fn.__name__}: {e}")
    print(f"{ok}/{len(fns)} tests OK")
    raise SystemExit(0 if ok == len(fns) else 1)
