from thirdparty.crystal import model_1d_to_d12
from utils.importer import Importer


def test_model_1d_to_d12(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang-charges' / 'critic2' / "cp-file.xyz")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model_1d_to_d12(model[0])) == 16285
