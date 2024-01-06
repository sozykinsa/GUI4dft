# -*- coding: utf-8 -*-
# Python 3

from src_core_atomistic.atomic_model import AtomicModel


def atomic_model_to_firefly_inp(model: AtomicModel) -> str:
    """Create file in Firefly *.inp format."""
    text = ""
    text += "!model \n $DATA\njob\nCn 1\n\n"
    text += model.coords_for_export("FireflyINP")
    return text
