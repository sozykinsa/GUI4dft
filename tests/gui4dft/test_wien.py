from src_gui4dft.program.wien import n_atoms_from_struct, alats_from_struct, atoms_from_struct


def test_n_atoms_from_struct(tests_path):
    f_name = str(tests_path / 'ref_data' / 'wien2k' / 'Fe53C_Si_1.struct')
    assert n_atoms_from_struct(f_name) == 55


def test_alats_from_struct(tests_path):
    f_name = str(tests_path / 'ref_data' / 'wien2k' / 'Fe53C_Si_1.struct')
    alats = alats_from_struct(f_name)
    assert alats[0] == 16.162604
    assert alats[3] == 90.000000


def test_atoms_from_struct(tests_path):
    f_name = str(tests_path / 'ref_data' / 'wien2k' / 'Fe53C_Si_1.struct')
    models = atoms_from_struct(f_name)
    assert models[0].n_atoms() == 55