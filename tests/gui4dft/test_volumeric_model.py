from src_gui4dft.program.gaussiancube import GaussianCube
from src_gui4dft.program.xsf import XSF
from src_gui4dft.program.volumericdatablock import VolumericDataBlock


def test_volumeric_data_block():
    model = VolumericDataBlock("IModel")
    assert model.title == "IModel"
    assert model.max is None
    assert model.min is None


def test_cube(tests_path):
    f_name = str(tests_path / 'ref_data' / 'siesta' / 'h2o-ang-charges' / 'cube_and_xsf' / "siesta.BADER.cube")
    model = GaussianCube()
    assert model.type == "TGaussianCube"
    model.parse(f_name)
    assert len(model.atoms) == 3
    assert len(model.blocks) == 1
    model.load_data("BADER:spin_1")
    assert model.Nx == 64


def test_xsf(tests_path):
    f_name = str(tests_path / 'ref_data' / 'siesta' / 'h2o-ang-charges' / 'cube_and_xsf' / "siesta.XSF")
    model = XSF()
    assert model.type == "TXSF"
    model.parse(f_name)
    assert len(model.atoms) == 3
    assert len(model.blocks) == 1
    model.load_data("BADER:spin_1")
    assert model.Nx == 30

    f_name = str(tests_path / 'ref_data' / 'incorrect' / "siesta-empty.XSF")
    model = XSF()
    assert model.type == "TXSF"
    model.parse(f_name)
    assert len(model.atoms) == 0
    assert len(model.blocks) == 0
    model.load_data("BADER:spin_1")
    assert model.Nx is None

    f_name = str(tests_path / 'ref_data' / 'incorrect' / "siesta-not-exist.XSF")
    model = XSF()
    assert model.type == "TXSF"
    model.parse(f_name)
    assert len(model.atoms) == 0
    assert len(model.blocks) == 0
    model.load_data("BADER:spin_1")
    assert model.Nx is None
