# -*- coding: utf-8 -*-

from src_gui4dft.models.hexagonal_plane import HexagonalPlane


class Graphene(HexagonalPlane):
    """The TGraphene class"""
    def __init__(self, n: int = 0, m: int = 0, length: float = 0):
        super().__init__(6, 6, 1.43, n, m, length)
