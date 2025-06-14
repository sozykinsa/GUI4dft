from src_gui4dft.program.crystal import model_1d_to_d12, model_2d_to_d12, energies
from src_gui4dft.program.importer_exporter import ImporterExporter


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


def test_energies(tests_path):
    f_name = str(tests_path / 'ref_data' / 'crystal' / 'corundum_optim' / "input.out")
    e = energies(f_name)
    assert e.size == 12
    assert e[0] == -38106.68336568802
