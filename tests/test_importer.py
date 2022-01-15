from utils.importer import Importer


def test_importer(tests_path):
    f_name = str(tests_path / 'ref_data' / "test_file_01.fdf")
    model, fdf = Importer.Import(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 96

