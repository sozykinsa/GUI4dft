# -*- coding: utf-8 -*-
from core_atomistic.atomic_model import AtomicModel


def model_to_octopus_input(model: AtomicModel):
    """
    C  0.000  1.396  0.000
    H -2.147  1.240  0.000
    """

    text = ""
    n_atoms = model.n_atoms()

    for i in range(n_atoms):
        text += str(model[i].let) + " " + model[i].xyz_string + "\n"
    return text
