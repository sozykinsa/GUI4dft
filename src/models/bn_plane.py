# -*- coding: utf-8 -*-

from models.hexagonal_plane import HexagonalPlane


class BNplane(HexagonalPlane):
    """The TGraphene class provides """
    def __init__(self, n: int = 0, m: int = 0, length: float = 0):
        super().__init__(5, 7, 1.45, n, m, length)
