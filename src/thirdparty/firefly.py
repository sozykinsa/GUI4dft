# -*- coding: utf-8 -*-
# Python 3

from utils import helpers
from models.atomic_model import TAtomicModel


def atomic_model_to_firefly_inp(model: TAtomicModel, filename: str) -> None:
    """Create file in Firefly *.inp format."""
    text = ""
    text += "!model \n $DATA\njob\nCn 1\n\n"
    text += model.coords_for_export("FireflyINP")
    helpers.write_text_to_file(filename, text)
