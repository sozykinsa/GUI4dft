from program.crystal import model_1d_to_d12, model_2d_to_d12
from utils.importer_exporter import ImporterExporter


def test_model_1d_to_d12(tests_path):
    f_name = str(tests_path / 'ref_data' / 'siesta' / 'h2o-ang' / "siesta.xyz")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    assert len(model_1d_to_d12(model[0])) == 140


def test_model_2d_to_d12(tests_path):
    f_name = str(tests_path / 'ref_data' / 'siesta' / 'h2o-ang' / "siesta.xyz")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    assert len(model_2d_to_d12(model[0])) == 154


def test_structure_opt_step(tests_path):
    f_name = str(tests_path / 'ref_data' / 'crystal' / 'corundum_optim' / "optc001")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    assert len(model[0].atoms) == 10
    f_name = str(tests_path / 'ref_data' / 'crystal' / 'h2o_optim' / "opta001")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    assert len(model[0].atoms) == 3

