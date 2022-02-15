from utils.importer import Importer
from utils.fdfdata import TFDFFile


def test_fdf_parser(tests_path):
    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.fdf")
    model, fdf = Importer.Import(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 32
    mesh = fdf.get_property("LatticeConstant")
    assert mesh == "1.0 Ang"
    bands = fdf.get_property("WriteBands")
    assert bands
    pulay = fdf.get_property("DM.NumberPulay")
    assert pulay == "4"
    spin = fdf.get_property("Spin")
    assert spin == "non-polarized"


def test_get_all_data(tests_path):
    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.fdf")
    model, fdf = Importer.Import(f_name, fl='all', prop=False, xyzcritic2=False)
    data = fdf.get_all_data(model[0], "Zmatrix Cartesian", "Ang", "LatticeParameters")
    assert len(data) > 0
