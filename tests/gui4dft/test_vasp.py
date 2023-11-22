from src_gui4dft.program.vasp import TVASP, model_to_vasp_poscar, fermi_energy_from_doscar


def test_model_to_vasp_poscar(h2o_model):
    text = model_to_vasp_poscar(h2o_model)
    assert len(text) == 216


def test_fermi_energy_from_doscar(tests_path):
    f_name = str(tests_path / 'ref_data' / 'vasp' / "DOSCAR")
    e_f = fermi_energy_from_doscar(f_name)
    assert e_f == 7.90341495


def test_volume(tests_path):
    f_name = str(tests_path / 'ref_data' / 'vasp' / "OUTCAR")
    v = TVASP.volume(f_name)
    assert v == 14.83


def test_energy_tot(tests_path):
    f_name = str(tests_path / 'ref_data' / 'vasp' / "OUTCAR")
    e, t, b = TVASP.energy_tot(f_name)
    assert e == -4.71040512


def test_abc(tests_path):
    f_name = str(tests_path / 'ref_data' / 'vasp' / "OUTCAR")
    a, b, c = TVASP.abc(f_name)
    assert abs(a - 2.757716447) < 1e-7
