# -*- coding: utf-8 -*-

from core_gui_atomistic.atomic_model import AtomicModel
from src_gui4dft.utils.importer_exporter import ImporterExporter
from pathlib import Path


class MetaGraphene(AtomicModel):
    """The meta graphene plane """
    def __init__(self, model_type: str = "irida-graphene", n=0, m=0):
        super().__init__()

        if model_type == "irida-graphene":
            f_name = str(Path(__file__).parent / "cells" / 'irida.fdf')

        if model_type == "psi-graphene":
            f_name = str(Path(__file__).parent / "cells" / 'psi-graphene.fdf')

        if model_type == "biphenylene":
            f_name = str(Path(__file__).parent / "cells" / 'biphenylene.fdf')

        if model_type == "tpdh-graphene":
            f_name = str(Path(__file__).parent / "cells" / 'tpdhg.fdf')

        basis, fdf = ImporterExporter.import_from_file(f_name, fl='all', prop=False)
        basis = basis[0]

        model = basis.grow_x(n)
        model = model.grow_y(m)
        self.atoms = model.atoms
        self.lat_vectors = model.lat_vectors