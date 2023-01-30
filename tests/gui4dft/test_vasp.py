from src_gui4dft.program.vasp import model_to_vasp_poscar, fermi_energy_from_doscar


def test_model_to_vasp_poscar(h2o_model):
    text = model_to_vasp_poscar(h2o_model)
    assert len(text) == 216


def test_fermi_energy_from_doscar(tests_path):
    f_name = str(tests_path / 'ref_data' / 'vasp' / "DOSCAR")
    e_f = fermi_energy_from_doscar(f_name)
    assert e_f == 7.90341495
