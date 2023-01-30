from src_gui4dft.program.crystal import model_1d_to_d12, model_2d_to_d12
from src_gui4dft.utils.importer_exporter import ImporterExporter


def test_model_1d_to_d12(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang' / "siesta.xyz")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    assert len(model_1d_to_d12(model[0])) == 140


def test_model_2d_to_d12(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang' / "siesta.xyz")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    assert len(model_2d_to_d12(model[0])) == 154
