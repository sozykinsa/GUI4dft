# -*- coding: utf-8 -*-
# Python 3

from models.atomic_model import TAtomicModel


def atomic_model_to_firefly_inp(model: TAtomicModel) -> None:
    """Create file in Firefly *.inp format."""
    text = ""
    text += "!model \n $DATA\njob\nCn 1\n\n"
    text += model.coords_for_export("FireflyINP")
    return text
