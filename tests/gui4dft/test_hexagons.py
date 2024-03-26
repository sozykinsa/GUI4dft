from carbon_hexa.carbon_structure import CarbonStructure, fill_tube
from models.swnt import SWNT


def test_distances() -> None:
    model = SWNT(3, 3, 0, 2)
    carb_model = CarbonStructure(model)
    distances = carb_model.distances(range(carb_model.n_atoms()))
    assert abs(distances[0][1] - 1.42819119) < 1e-4
    assert abs(distances[0][13] - 1.42819119) < 1e-4


def test_carbon_structure() -> None:
    model = SWNT(3, 3, 0, 4)
    carb_model = CarbonStructure(model)
    hexagons = carb_model.hexagons_of_swnt()
    assert len(hexagons) == 24


def test_fill_tube():
    rad_tube = 5.0
    length = 6.0
    n_atoms = 8
    rad_atom = 0.3
    delta = 1.2
    n_prompts = 1
    let = "Li"
    charge = 3
    models = fill_tube(rad_tube, length, n_atoms, rad_atom, delta, n_prompts, let, charge)
    assert len(models) == 1
