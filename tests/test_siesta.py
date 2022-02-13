from utils.siesta import TSIESTA


def test_siesta_lattice(tests_path):
    f_name = str(tests_path / 'ref_data' / "test_file_01.fdf")
    lat1, lat2, lat3 = TSIESTA.lattice_vectors(f_name)
    assert lat1 == [False, False, False]

    a = 1
    b = 2
    c = 3
    lat1, lat2, lat3 = TSIESTA.lat_vectors_from_params(a, b, c, 90, 90, 90)
    assert lat1 == [1, 0, 0]

    lat1, lat2, lat3 = TSIESTA.lattice_parameters_abc_angles(f_name)
    assert lat1 == [90.0, 0.0, 0.0]
    assert lat2 == [0.0, 90.0, 0.0]
    assert lat3 == [0.0, 0.0, 12.2833]


def test_energy_tot(tests_path):
    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.out")
    e_tot = TSIESTA.energy_tot(f_name)
    assert e_tot == -4965.062613

    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta2.out")
    e_tot = TSIESTA.energy_tot(f_name)
    assert e_tot is None


def test_energies(tests_path):
    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.out")
    energies = TSIESTA.energies(f_name)
    assert len(energies) == 8


def test_spin_polarized(tests_path):
    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.out")
    assert not TSIESTA.spin_polarized(f_name)
