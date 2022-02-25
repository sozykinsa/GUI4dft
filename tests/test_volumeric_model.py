from models.gaussiancube import GaussianCube
from models.volumericdatablock import VolumericDataBlock


def test_volumeric_data_block():
    model = VolumericDataBlock("IModel")
    assert model.title == "IModel"
    assert model.max is None
    assert model.min is None


def test_cube(tests_path):
    f_name = str(tests_path / 'ref_data' / 'h2o-ang-charges' / 'cube_and_xsf' / "siesta.XSF")
    model = GaussianCube()
    assert model.type == "TGaussianCube"

