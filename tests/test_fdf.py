from utils.importer import Importer


def test_fdf_parser(tests_path):
    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.fdf")
    model, fdf = Importer.Import(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 32
