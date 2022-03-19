# -*- coding: utf-8 -*-

import math

from models.atom import Atom
from models.atomic_model import TAtomicModel


class SWGNT(TAtomicModel):
    """The SWGNT class provides """
    def __init__(self, n, m, length=0, n_cell=1):
        super().__init__()
        a: float = 2.9

        t = math.sqrt(1.0 * n * n+1.0 * n * m+1.0 * m * m)
        a11 = (2.0 * n+m) / (2.0 * t)

        if length < 1e-3:
            length = t

        a12 = math.sqrt(3.0) * m / (2.0 * t)
        r1 = a * t / (2 * math.pi)
        r = a / (2.0 * math.sin(math.pi / t))

        border = 20
        selector = 1

        for i in range(-border, border):
            j = -border
            while j < border:
                selector = 1-selector
                if selector:
                    x = i * a
                    y = math.sqrt(3.0) * j * a
                else:
                    x = (i+0.5) * a
                    y = math.sqrt(3.0) * (0.5+j) * a

                x1 = a11 * x + a12 * y
                y1 = -a12 * x + a11 * y
                if (x1 >= -1e-5) and (x1-a * t < -1e-5) and (y1 >= -1e-5) and (y1 <= length):
                    qx = r * math.cos(-x1 / r1)
                    qy = r * math.sin(-x1 / r1)
                    qz = y1
                    # graphene
                    # else {
                    #    dot[count].x= (float) x1;
                    #    dot[count].y= (float) y1;
                    #    dot[count].z= 0.0;
                    #    }
                    # dot[count].select = 0;

                    self.add_atom(Atom([qx, qy, qz, "Au", 79]))

                j += selector
