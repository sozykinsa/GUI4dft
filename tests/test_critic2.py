from thirdparty.critic2 import check_cro_file
from utils.importer import Importer


def test_open_xyz_critic_file(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang-charges' / 'critic2' / "cp-file.xyz")
    model, fdf = Importer.Import(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 301
    model, fdf = Importer.Import(f_name, fl='all', prop=False, xyzcritic2=True)
    assert len(model[0].atoms) == 3


def test_create_critic2_xyz_file(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang-charges' / 'critic2' / "cp-file.xyz")
    model, fdf = Importer.Import(f_name, fl='all', prop=False, xyzcritic2=True)
    assert len(model[0].bcp) == 5


def test_atoms_of_bond_path(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang-charges' / 'critic2' / "cp-file.xyz")
    model, fdf = Importer.Import(f_name, fl='all', prop=False, xyzcritic2=True)
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

