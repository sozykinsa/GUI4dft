from src_gui4dft.program.vasp import VASP


def test_atoms_from_poscar(tests_path):
    f_name = str(tests_path / 'ref_data' / 'vasp' / 'vasp_direct' / "POSCAR")
    model = VASP.atoms_from_poscar(f_name)[0]
    assert model.n_atoms() == 4

    f_name = str(tests_path / 'ref_data' / 'vasp' / 'vasp_cartesian' / "POSCAR")
    model = VASP.atoms_from_poscar(f_name)[0]
    assert model.n_atoms() == 1

    f_name = str(tests_path / 'ref_data' / 'vasp' / 'vasp_selective' / "POSCAR")
    model = VASP.atoms_from_poscar(f_name)[0]
    assert model.n_atoms() == 4


def test_atoms_from_outcar(tests_path):
    f_name = str(tests_path / 'ref_data' / 'vasp' / 'vasp_cartesian' / "OUTCAR")
    vasp = VASP()
    model = vasp.atoms_from_outcar(f_name)[0]
    assert len(model.atoms) == 1


def test_specieses_from_outcar(tests_path):
    f_name = str(tests_path / 'ref_data' / 'vasp' / 'vasp_cartesian'/ "OUTCAR")
    specieses = VASP.specieses_from_outcar(f_name)
    assert len(specieses) == 1
    assert specieses[0] == 'Si'


def test_model_to_vasp_poscar(h2o_model):
    text = VASP.model_to_vasp_poscar(h2o_model)
    assert len(text) == 208
    text = VASP.model_to_vasp_poscar(h2o_model, coord_type="Cartesian")
    assert len(text) == 211


def test_fermi_energy_from_doscar(tests_path):
    f_name = str(tests_path / 'ref_data' / 'vasp' / 'vasp_cartesian' / "DOSCAR")
    e_f = VASP.fermi_energy_from_doscar(f_name)
    assert e_f == 7.90341495


def test_n_atoms(tests_path):
    f_name = str(tests_path / 'ref_data' / 'vasp' / 'vasp_cartesian'/ "POSCAR")
    n = VASP.number_of_atoms(f_name)
    assert n == 1


def test_vasp_latt_const(tests_path):
    f_name = str(tests_path / 'ref_data' / 'vasp' / 'vasp_direct' / "POSCAR")
    lat_const = VASP.vasp_latt_const(f_name)
    assert lat_const == 1.0


def test_volume(tests_path):
    f_name = str(tests_path / 'ref_data' / 'vasp' / 'vasp_cartesian' / "OUTCAR")
    v = VASP.volume(f_name)
    assert v == 14.83


def test_energy_tot(tests_path):
    f_name = str(tests_path / 'ref_data' / 'vasp' / 'vasp_cartesian' / "OUTCAR")
    e, t, b = VASP.energy_tot(f_name)
    assert e == -4.71040512


def test_vectors(tests_path):
    f_name = str(tests_path / 'ref_data' / 'vasp' / 'vasp_cartesian' / "OUTCAR")
    vecs = VASP.vectors_from_outcar(f_name)
    print(vecs[0][0])
    a = vecs[0][0][0]
    assert abs(a - 1.95) < 1e-2


def test_abc(tests_path):
    f_name = str(tests_path / 'ref_data' / 'vasp' / 'vasp_cartesian' / "OUTCAR")
    vasp = VASP()
    a, b, c = vasp.abc_from_outcar(f_name)
    assert abs(a - 2.757716447) < 1e-7
