from utils.importer import Importer


def test_importer_fdf(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang' / "siesta.fdf")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-bohr' / "siesta.fdf")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-bohr' / "siesta-params.fdf")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-bohr' / "siesta-without-cell.fdf")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-zmatrix' / "siesta.fdf")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 3


def test_importer_ani(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang' / "siesta.ANI")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=False, xyzcritic2=False)
    # no file
    assert len(model) == 0

    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.ANI")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=False, xyzcritic2=False)
    # no file
    assert len(model[0].atoms) == 32


def test_importer_output(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang' / "siesta.out")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=True, xyzcritic2=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-bohr' / "siesta.out")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=True, xyzcritic2=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-zmatrix' / "siesta.out")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=True, xyzcritic2=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'siesta4-md' / "siesta.out")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=True, xyzcritic2=False)
    assert len(model[0].atoms) == 119

    f_name = str(tests_path / 'ref_data' / 'h2o-ang-charges' / "siesta.out")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=True, xyzcritic2=False)
    assert len(model[0].atoms) == 3
    atom = model[-1].atoms[0]
    assert atom.getProperty("charge Voronoi") == 0.091
    assert atom.getProperty("charge Hirshfeld") == 0.12
    assert atom.getProperty("charge Mulliken") == -0.134


def test_importer_xyz(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang' / "siesta.xyz")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-bohr' / "siesta.xyz")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-zmatrix' / "siesta.xyz")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / "xmol.xyz")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 6


def test_importer_struct_out(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang' / "siesta.STRUCT_OUT")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-bohr' / "siesta.STRUCT_OUT")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-zmatrix' / "siesta.STRUCT_OUT")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 3
    atom = model[-1].atoms[0]
    assert atom.getProperty("charge Voronoi") is None


def test_importer_md_car(tests_path):
    f_name = str(tests_path / 'ref_data' / 'siesta4-md' / "C112.MD_CAR")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 119


def test_importer_cube(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang-charges' / 'cube_and_xsf' / "siesta.BADER.cube")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 3


def test_importer_xsf(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang-charges' / 'cube_and_xsf' / "siesta.XSF")
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 3


def test_importer_check_dos_pdos_bands(tests_path):
    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.out")

    dos_file, e_fermy = Importer.check_dos_file(f_name)
    assert e_fermy == -4.804823
    assert dos_file.endswith("siesta.DOS")

    pdos_file = Importer.check_pdos_file(f_name)
    assert pdos_file.endswith("siesta.PDOS")

    bands_file = Importer.check_bands_file(f_name)
    assert bands_file.endswith("siesta.bands")


def test_importer_poscar(tests_path):
    f_name = str(tests_path / 'ref_data' / 'vasp' / 'POSCAR')
    model, fdf = Importer.import_from_file(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 1
