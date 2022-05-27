from thirdparty.critic2 import check_cro_file, create_critic2_xyz_file, create_cri_file
from utils.importer import Importer


def test_open_xyz_critic_file(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang-charges' / 'critic2' / "cp-file.xyz")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 301
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=False, xyzcritic2=True)
    assert len(model[0].atoms) == 3


def test_create_critic2_xyz_file(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang-charges' / 'critic2' / "cp-file.xyz")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=False, xyzcritic2=True)
    assert len(model[0].bcp) == 5
    text = create_critic2_xyz_file(model[0].bcp, (model[0].bcp[1], model[0].bcp[2]), True, model[0])
    assert len(text) == 3739
    text = create_critic2_xyz_file(model[0].bcp, (model[0].bcp[1], model[0].bcp[2]), False, model[0])
    assert len(text) == 8375


def test_atoms_of_bond_path(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang-charges' / 'critic2' / "cp-file.xyz")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=False, xyzcritic2=True)
    atom1, atom2 = model[0].atoms_of_bond_path(1)
    assert atom1 == 2
    assert atom2 == 2

    atom1, atom2 = model[0].atoms_of_bond_path(2)
    assert atom1 == 1
    assert atom2 == 1


def test_check_cro_file(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang-charges' / 'critic2' / "siesta-1-cp.cro")
    box_bohr, box_ang, box_deg, cps = check_cro_file(f_name)
    assert len(box_bohr) == 3
    f_name = str(tests_path / 'ref_data' / 'h2o-ang-charges' / 'critic2' / "siesta-1-cp-error.cro")
    box_bohr, box_ang, box_deg, cps = check_cro_file(f_name)
    assert len(box_bohr) == 0


def test_create_cri_file(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang-charges' / 'critic2' / "cp-file.xyz")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=False, xyzcritic2=True)
    textl, lines, te, text = create_cri_file((1, 2), 1, True, model[0], "")
    assert len(textl) == 234
    textl, lines, te, text = create_cri_file((1, 2), 1, False, model[0], "")
    assert len(textl) == 234
