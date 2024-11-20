# -*- coding: utf-8 -*-

import math
import numpy as np
from core_atomistic.atom import Atom
from core_atomistic.atomic_model import AtomicModel


class TrigonalPlane(AtomicModel):
    """The TrigonalPlane """

    def __init__(self, n, m):
        super().__init__()
        a: float = 2.9

        basis = AtomicModel()
        basis.add_atom(Atom([0.0, 0.0, 0.0, "Au", 79]))
        v1 = a * np.array([1.0, 0.0, 0.0])
        v2 = a * np.array([-0.5, math.sqrt(3.0) / 2.0, 0.0])
        v3 = np.array([0.0, 0.0, 10.0])
        basis.set_lat_vectors(v1, v2, v3)

        model = basis.grow_x(n)
        model = model.grow_y(m)
        self.atoms = model.atoms
        self.lat_vectors = model.lat_vectors
