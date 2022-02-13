from utils.electronic_prop_reader import read_siesta_bands
from utils.calculators import gaps


def test_bands(tests_path):
    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.bands")

    kmin, kmax = 0.0, 0.39
    is_check_bands_spin = True
    bands, emaxf, eminf, homo, kmesh, lumo, xticklabels, xticks = read_siesta_bands(f_name, is_check_bands_spin,
                                                                                        kmax, kmin)
    assert len(kmesh) == 100

    gap, gap_ind = gaps(bands, emaxf, eminf, homo, lumo)
    assert gap == 0.6385999999999994

