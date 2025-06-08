import numpy as np
import pytest

from src_gui4dft.utils.calculators import Calculators


def test_lattice_approx():
    data = [[2.44, -3721.954963], [2.444, -3721.957231], [2.445, -3721.957265], [2.446, -3721.957066],
            [2.45, -3721.953855]]
    params, x_data, y_data = Calculators.approx_parabola(data)
    assert np.array(params) == pytest.approx(np.array([-3039.65306723,  -558.23175345,   114.18025869]))

    params, x_data, y_datat = Calculators.approx_murnaghan(data)
    assert np.array(params) == pytest.approx(np.array([-3.72195729e+03,  5.58231753e+02,  4.0,  2.44451957]), rel=5e-3)

    params, x_data, y_data = Calculators.approx_birch_murnaghan(data)
    assert np.array(params) == pytest.approx(np.array([-3.72195729e+03,  5.58780686e+02,  4.0,  2.44451159]), rel=5e-3)

