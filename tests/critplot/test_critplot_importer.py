from src_critplot.interface.io import ImporterExporter
from core_atomistic import helpers


def test_check_format(tests_path):
    assert helpers.check_format(str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta1.out")) == "unknown"
    assert helpers.check_format(str(tests_path / 'ref_data' / 'critic2' / "siesta-1-cp.cro")) == "critic_cro"
    format1 = helpers.check_format(str(tests_path / 'ref_data' / 'topond' / 'co2-crystal' / 'topo-ex1' / "output.outp"))
    assert format1 == "topond_out"


def test_importer_cro(tests_path):
    f_name = str(tests_path / 'ref_data' / 'critic2' / "siesta-1-cp.cro")
    model, fl = ImporterExporter.import_from_file(f_name)
    assert len(model[0].atoms) == 6
    model[0].translated_atoms_remove()
    assert len(model[0].atoms) == 3


def test_importer_outp(tests_path):
    f_name = str(tests_path / 'ref_data' / 'topond' / 'co2-crystal' / 'topo-ex1' / "output.outp")
    model, fl = ImporterExporter.import_from_file(f_name)
    assert len(model[0].atoms) == 6
    model[0].translated_atoms_remove()
    assert len(model[0].atoms) == 6
