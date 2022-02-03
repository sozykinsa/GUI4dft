from utils.importer import Importer


def test_importer_fdf(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang' / "siesta.fdf")
    model, fdf = Importer.Import(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-bohr' / "siesta.fdf")
    model, fdf = Importer.Import(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-zmatrix' / "siesta.fdf")
    model, fdf = Importer.Import(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 3


def test_importer_output(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang' / "siesta.out")
    model, fdf = Importer.Import(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-bohr' / "siesta.out")
    model, fdf = Importer.Import(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-zmatrix' / "siesta.out")
    model, fdf = Importer.Import(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 3


def test_importer_xyz(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang' / "siesta.xyz")
    model, fdf = Importer.Import(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-bohr' / "siesta.xyz")
    model, fdf = Importer.Import(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-zmatrix' / "siesta.xyz")
    model, fdf = Importer.Import(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 3


def test_importer_struct_out(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang' / "siesta.STRUCT_OUT")
    model, fdf = Importer.Import(f_name, fl='all', prop=True, xyzcritic2=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-bohr' / "siesta.STRUCT_OUT")
    model, fdf = Importer.Import(f_name, fl='all', prop=True, xyzcritic2=False)
    assert len(model[0].atoms) == 3

    f_name = str(tests_path / 'ref_data' / 'h2o-zmatrix' / "siesta.STRUCT_OUT")
    model, fdf = Importer.Import(f_name, fl='all', prop=True, xyzcritic2=False)
    assert len(model[0].atoms) == 3


def test_importer_cube(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang-charges' / 'cube_and_xsf' / "siesta.BADER.cube")
    model, fdf = Importer.Import(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 3


def test_importer_xsf(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang-charges' / 'cube_and_xsf' / "siesta.XSF")
    model, fdf = Importer.Import(f_name, fl='all', prop=False, xyzcritic2=False)
    assert len(model[0].atoms) == 3
