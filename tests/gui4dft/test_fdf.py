from src_gui4dft.program.importer_exporter import ImporterExporter


def test_fdf_parser(tests_path):
    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.fdf")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    assert len(model[0].atoms) == 32
    mesh = fdf.get_property("LatticeConstant")
    assert mesh == "1.0 Ang"
    bands = fdf.get_property("WriteBands")
    assert bands
    pulay = fdf.get_property("DM.NumberPulay")
    assert pulay == "4"
    pulay_er = fdf.get_property("DN.NumberPulay")
    assert pulay_er == ""
    spin = fdf.get_property("Spin")
    assert spin == "non-polarized"
    basis_sizes = fdf.get_block("PAO.BasisSizes")
    assert basis_sizes[0] == "    C\tDZP\n"


def test_get_all_data(tests_path):
    f_name = str(tests_path / 'ref_data' / 'swcnt(8,0)' / "siesta.fdf")
    model, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
    data = fdf.get_all_data(model[0], "Zmatrix Cartesian", "Ang", "LatticeParameters")
    assert len(data) > 0
