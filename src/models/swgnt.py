# -*- coding: utf-8 -*-

import math

from models.atom import Atom
from models.atomic_model import TAtomicModel


class SWGNT(TAtomicModel):
    """The SWGNT class provides """
    def __init__(self, n, m, leng=0, ncell=1):
        super().__init__()
        a: float = 2.9

        # if ((type == 2) | | (type == 6)) {
        t = math.sqrt(1.0 * n * n+1.0 * n * m+1.0 * m * m)
        A11 = (2.0 * n+m) / (2.0 * t)

        #if (type == 3) {
        #t = math.sqrt(1.0 * n * n-1.0 * n * m+1.0 * m * m)
        #A11 = (2.0 * n-m) / (2.0 * t)

        if leng < 1e-3:
            leng = t

        A12 = math.sqrt(3.0) * m / (2.0 * t)
        R1 = a * t / (2 * math.pi)
        R = a / (2.0 * math.sin(math.pi / t))
        nam_at = 0

        border = 20
        selector = 1


        # start
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

                x1 = A11 * x + A12 * y
                y1 = -A12 * x + A11 * y
                if (x1 >= -1e-5) and (x1-a * t < -1e-5) and (y1 >= -1e-5) and (y1 <= leng):
                    nam_at += 1

                j += selector

        #dot = new atom[nam_at]
        count = 0

        for i in range(-border, border):
            j = -border
            while j < border:
                #{
                selector = 1-selector
                if selector:
                    x = i * a
                    y = math.sqrt(3.0) * j * a
                else:
                    x = (i+0.5) * a
                    y = math.sqrt(3.0) * (0.5+j) * a

                x1 = A11 * x + A12 * y
                y1 = -A12 * x + A11 * y
                if (x1 >= -1e-5) and (x1-a * t < -1e-5) and (y1 >= -1e-5) and (y1 <= leng):
                    #{
                    qx = R * math.cos(-x1 / R1)
                    qy = R * math.sin(-x1 / R1)
                    qz = y1
                    # graphene
                    #else {
                    #    dot[count].x= (float) x1;
                    #    dot[count].y= (float) y1;
                    #    dot[count].z= 0.0;
                    #    }
                    #dot[count].select = 0;

                    self.add_atom(Atom([qx, qy, qz, "Au", 79]))

                    #count++;
                    #}
                #}

                j += selector

        size = count

        #stop


        #if leng == 0:
        #    leng = ncell * SWNT.unitlength(n, m, 1.43)

        #Graphene.__init__(self)

        #rad = SWNT.radius(n, m)
        #self.set_lat_vectors([10 * rad, 0, 0], [0, 10 * rad, 0], [0, 0, leng])
        #np1, pi, px, py, leng = self.graphene_positions(n, m, leng)

        """ output """
        #R = leng / (2 * math.pi)
        
        #for i_par in range(0, np1):
        #    phi_par = px[i_par] / R
        #    qx = R * math.sin(phi_par)
        #    qy = -R * math.cos(phi_par)
        #    qz = py[i_par]
        #    self.add_atom(Atom([qx, qy, qz, "C", 6]))

        """
        sort();
        for (int j=0;j<size;j++) dot[j].num = j+1;  
        """

    #@staticmethod
    #def radius(n, m):
    #    return math.sqrt(n * n + n * m + m * m)

    #@staticmethod
    #def unitlength(n, m, acc):
    #    a = math.sqrt(3) * acc
    #    pi = math.pi
        
    #    b1x = 2 * pi / a / math.sqrt(3)
    #    b1y = 2 * pi / a
    #    b2x = 2 * pi / a / math.sqrt(3)
    #    b2y = -2 * pi / a
    #    Ch = a * math.sqrt(n * n + n * m + m * m)
    #    dia = Ch / pi
    #    theta = math.atan((math.sqrt(3) * m / (2.0 * n + m)))
    #    theta = theta * 180.0 / pi
    #    d = helpers.cdev(n, m)
    #    if (n - m) % (3 * d) != 0:
    #        dR = d
    #    else:
    #        dR = 3 * d
    #    T1 = (2 * m + n) / dR
    #    T2 = -(2 * n + m) / dR
    #    T = math.sqrt(3) * Ch / dR
    #    return T
