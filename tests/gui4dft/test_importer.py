import numpy as np

from src_gui4dft.utils.importer_exporter import ImporterExporter
from core_gui_atomistic import helpers


def test_check_format(tests_path):
    assert helpers.check_format(str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta1.out")) == "unknown"
    assert helpers.check_format(str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.out")) == "SIESTAout"
    assert helpers.check_format(str(tests_path / 'ref_data' / 'h2o-ang' / "siesta.fdf")) == "SIESTAfdf"
    assert helpers.check_format(str(tests_path / 'ref_data' / 'vasp' / 'POSCAR')) == "VASPposcar"
    assert helpers.check_format(str(tests_path / 'ref_data' / 'qe' / 'si-scf' / "pw.out")) == "QEPWout"
    file1 = str(tests_path / 'ref_data' / 'h2o-ang-charges' / 'cube_and_xsf' / "siesta.BADER.cube")
    assert helpers.check_format(file1) == "GAUSSIAN_cube"
    assert helpers.check_format(str(tests_path / 'ref_data' / 'wien2k' / 'Fe53C_Si_1.struct')) == "WIENstruct"


def test_importer_fdf(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang' / "siesta.fdf")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-scaled' / "siesta.fdf")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-bohr' / "siesta.fdf")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-bohr' / "siesta-params.fdf")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-bohr' / "siesta-without-cell.fdf")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-zmatrix' / "siesta.fdf")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'incorrect' / "siesta-no-cell.fdf")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    assert len(model[0].atoms) == 3


def test_importer_ani(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang' / "siesta.ANI")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    # no file
    assert len(model) == 0

    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.ANI")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    # no file
    assert len(model[0].atoms) == 32


def test_importer_output(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang' / "siesta.out")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=True)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-bohr' / "siesta.out")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=True)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-zmatrix' / "siesta.out")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=True)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'siesta4-md' / "siesta.out")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=True)
    assert len(model[0].atoms) == 119

    f_name = str(tests_path / 'ref_data' / 'h2o-ang-charges' / "siesta.out")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=True)
    assert len(model[0].atoms) == 3
    atom = model[-1].atoms[0]
    assert atom.get_property("charge Voronoi") == 0.091
    assert atom.get_property("charge Hirshfeld") == 0.12
    assert atom.get_property("charge Mulliken") == -0.134


def test_importer_ghost(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang-ghost' / "siesta.fdf")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=True)
    assert len(model[0].atoms) == 3
    assert model[0].get_tags()[1] == -1
    f_name = str(tests_path / 'ref_data' / 'h2o-ang-ghost' / "siesta.out")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=True)
    assert len(model[0].atoms) == 3
    assert model[0].get_tags()[1] == -1


def test_importer_xyz(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang' / "siesta.xyz")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-bohr' / "siesta.xyz")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-zmatrix' / "siesta.xyz")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / "xmol.xyz")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    assert len(model[0].atoms) == 6


def test_importer_struct_out(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang' / "siesta.STRUCT_OUT")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-bohr' / "siesta.STRUCT_OUT")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-zmatrix' / "siesta.STRUCT_OUT")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    assert len(model[0].atoms) == 3
    atom = model[-1].atoms[0]
    assert atom.get_property("charge Voronoi") is None


def test_importer_md_car(tests_path):
    f_name = str(tests_path / 'ref_data' / 'siesta4-md' / "C112.MD_CAR")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    assert len(model[0].atoms) == 119


def test_importer_cube(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang-charges' / 'cube_and_xsf' / "siesta.BADER.cube")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    assert len(model[0].atoms) == 3


def test_importer_xsf(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang-charges' / 'cube_and_xsf' / "siesta.XSF")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    assert len(model[0].atoms) == 3


def test_importer_check_dos_pdos_bands(tests_path):
    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.out")

    dos_file, e_fermy = ImporterExporter.check_dos_file(f_name)
    assert e_fermy == -4.804823
    assert dos_file.endswith("siesta.DOS")

    pdos_file = ImporterExporter.check_pdos_file(f_name)
    assert pdos_file.endswith("siesta.PDOS")

    bands_file = ImporterExporter.check_bands_file(f_name)
    assert bands_file.endswith("siesta.bands")


def test_importer_poscar(tests_path):
    f_name = str(tests_path / 'ref_data' / 'vasp' / 'POSCAR')
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    assert len(model[0].atoms) == 1
