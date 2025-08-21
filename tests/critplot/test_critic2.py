from src_critplot.programs.critic2 import Critic2ModelCP


def test_critic2_model_cp_constructor(tests_path):
    f_name = str(tests_path / 'ref_data' / 'critic2' / "siesta-1-cp.cro")
    model = Critic2ModelCP(f_name)
    n = model.n_atoms()
    assert n == 6


def test_atoms_of_bond_path(tests_path):
    f_name = str(tests_path / 'ref_data' / 'critic2' / "siesta-1-cp.cro")
    model = Critic2ModelCP(f_name)
    atom1, atom2 = model.atoms_of_bond_path(model.cps[1])
    assert atom1 is None
    assert atom2 is None

    atom1, atom2 = model.atoms_of_bond_path(model.cps[2])
    assert atom1 is None
    assert atom2 is None

    atom1, atom2 = model.atoms_of_bond_path(model.cps[3])
    assert atom1 == 3
    assert atom2 == 3

    atom1, atom2 = model.atoms_of_bond_path(model.cps[4])
    assert atom1 == 3
    assert atom2 == 3

    atom1, atom2 = model.atoms_of_bond_path(model.cps[5])
    assert atom1 == 2
    assert atom2 == 1


def test_critical_points(tests_path):
    f_name = str(tests_path / 'ref_data' / 'critic2' / "siesta-1-cp.cro")
    model = Critic2ModelCP(f_name)
    assert len(model.cps) == 11
    assert model.cps[5].get_property("cp_bp_len") == 3.4582895082860503
