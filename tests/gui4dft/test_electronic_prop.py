from utils.electronic_prop_reader import read_siesta_bands, dos_from_file, dos_siesta_vert
from program.vasp import vasp_dos
from program.siesta import TSIESTA

from utils.calculators import gaps


def test_dos_from_file(tests_path):
    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.DOS")
    spin_up, spin_down, energy = dos_from_file(f_name)
    assert len(energy) == 1000

    f_name = str(tests_path / 'ref_data' / 'vasp' / "DOSCAR")
    spin_up, spin_down, energy = vasp_dos(f_name)
    assert len(energy) == 301


def test_dos_siesta_vert(tests_path):
    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.DOS")
    data = dos_siesta_vert(f_name)
    assert len(data) == 1000
    assert len(data[0]) == 2


def test_pdos(tests_path):
    atom_index = range(1, 33)
    species = ['C']
    number_l = [0, 1, 2, 3, 4, 5, 6, 7]
    number_m = [-7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7]
    number_n = [1, 2, 3, 4, 5, 6, 7, 8]
    number_z = [1, 2, 3, 4, 5]

    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.PDOS")
    pdos, energy = TSIESTA.calc_pdos(f_name, atom_index, species, number_l, number_m, number_n, number_z)
    assert len(energy) == 1000

    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)spin_polarized' / "siesta.PDOS")
    pdos, energy = TSIESTA.calc_pdos(f_name, atom_index, species, number_l, number_m, number_n, number_z)
    assert len(energy) == 1000


def test_bands(tests_path):
    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.bands")

    kmin, kmax = 0.0, 0.39
    is_check_bands_spin = True
    bands, emaxf, eminf, homo, kmesh, lumo, xticklabels, xticks = read_siesta_bands(f_name, is_check_bands_spin,
                                                                                    kmax, kmin)
    assert len(kmesh) == 100

    gap, gap_ind = gaps(bands, emaxf, eminf, homo, lumo)
    assert gap == 0.6385999999999994

    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)spin_polarized' / "siesta.bands")

    kmin, kmax = 0.0, 0.39
    is_check_bands_spin = True
    bands, emaxf, eminf, homo, kmesh, lumo, xticklabels, xticks = read_siesta_bands(f_name, is_check_bands_spin,
                                                                                    kmax, kmin)
    assert len(kmesh) == 100

    gap, gap_ind = gaps(bands, emaxf, eminf, homo, lumo)
    assert gap == 0.6385999999999994
