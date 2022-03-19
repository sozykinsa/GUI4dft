# -*- coding: utf-8 -*-
# Python 3

from models.atomic_model import TAtomicModel


def atomic_model_to_firefly_inp(model: TAtomicModel, filename: str) -> None:
    """Create file in Firefly *.inp format."""
    f = open(filename, 'w')
    data = ""
    data += "!model \n $DATA\njob\nCn 1\n\n"
    data += model.coords_for_export("FireflyINP")
    print(data, file=f)
    f.close()
