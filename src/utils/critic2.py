# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
sys.path.append('.')


def create_critic2_xyz_file(bcp, bcp_seleсted, fname, is_with_selected, model):
    if is_with_selected:
        text = model.toCriticXYZfile(bcp_seleсted)
    else:
        for b in bcp_seleсted:
            for cp in bcp:
                if cp.to_string() == b.to_string():
                    bcp.remove(cp)
        text = model.toCriticXYZfile(bcp)



def create_cri_file(cp_list, extra_points, fname, is_form_bp, model, text_prop):
    sys_coord = np.array([model.LatVect1, model.LatVect2, model.LatVect3])
    obr = np.linalg.inv(sys_coord).transpose()
    text = ""
    te = ""
    lines = ""
    textl = "crystal model.BADER.cube\n"
    textl += "WRITE model.xyz\n"
    textl += "load model.BADER.cube\n"
    textl += "load model.VT.DN.cube\n"
    textl += "load model.VT.UP.cube\n"
    textl += 'LOAD AS "-$2-$3"\n'
    textl += 'LOAD AS LAP 1\n'
    textl += "REFERENCE 1\n"
    for ind in range(0, len(cp_list)):
            cp = cp_list[ind]
            text += "Bond Critical Point: " + str(ind) + "  :  "
            ind1, ind2 = model.atoms_of_bond_path(ind)
            atom1 = model.atoms[ind1].let + str(ind1)
            atom2 = model.atoms[ind2].let + str(ind2)
            title = atom1 + "-" + atom2
            text += title + "\n"

            if is_form_bp:
                """ bond path """
                bond1 = cp.getProperty("bond1")
                bond2 = cp.getProperty("bond2")

                path_low = []
                for i in range(0, len(bond1)):
                    Coord = np.array(
                        [bond1[len(bond1) - i - 1].x, bond1[len(bond1) - i - 1].y, bond1[len(bond1) - i - 1].z])
                    res = obr.dot(Coord)
                    path_low.append(np.array([float(res[0]), float(res[1]), float(res[2])]))

                from_to = "{0:14.10} {1:14.10} {2:14.10} {3:14.10} {4:14.10} {5:14.10} ".format(path_low[0][0],
                                                                                                path_low[0][1],
                                                                                                path_low[0][2],
                                                                                                path_low[-1][0],
                                                                                                path_low[-1][1],
                                                                                                path_low[-1][2])

                lines += "# " + title + "\n"
                lines += "REFERENCE 1\n"
                lines += "LINE " + from_to + " 100 FILE ./lines/lines-" + title + "-00-charge.txt\n"
                lines += "REFERENCE 4\n"
                lines += "LINE " + from_to + " 100 FILE ./lines/lines-" + title + "-00-elpot.txt\n"
                lines += "REFERENCE 5\n"
                lines += "LINE " + from_to + " 100 FILE ./lines/lines-" + title + "-00-lapl.txt\n"

                first = "{0:14.10} {1:14.10} {2:14.10} ".format(path_low[-1][0], path_low[-1][1], path_low[-1][2])

                for i in range(1, len(bond2)):
                    Coord = np.array([bond2[i].x, bond2[i].y, bond2[i].z])
                    res = obr.dot(Coord)
                    path_low.append(np.array([float(res[0]), float(res[1]), float(res[2])]))

                last = "{0:14.10} {1:14.10} {2:14.10} ".format(path_low[-1][0], path_low[-1][1], path_low[-1][2])
                lines += "REFERENCE 1\n"
                lines += "LINE " + first + last + " 100 FILE ./lines/lines-" + title + "-01-charge.txt\n"
                lines += "REFERENCE 4\n"
                lines += "LINE " + first + last + " 100 FILE ./lines/lines-" + title + "-01-elpot.txt\n"
                lines += "REFERENCE 5\n"
                lines += "LINE " + first + last + " 100 FILE ./lines/lines-" + title + "-01-lapl.txt\n"

                path_fine = [path_low[0]]
                for i in range(1, len(path_low)):
                    dv = (path_low[i] - path_low[i - 1]) / extra_points
                    for j in range(0, extra_points):
                        path_fine.append(path_fine[-1] + dv)

                for i in range(0, len(path_fine)):
                    text += "{0:20.16f} {1:20.16f} {2:20.16f}\n".format(path_fine[i][0], path_fine[i][1],
                                                                        path_fine[i][2])
                    te += "{0:20.16f} {1:20.16f} {2:20.16f}\n".format(path_fine[i][0], path_fine[i][1], path_fine[i][2])
            else:
                """ critical points only """
                Coord = np.array([cp.x, cp.y, cp.z])
                res = obr.dot(Coord)
                text += "{0:20.16f} {1:20.16f} {2:20.16f}\n".format(float(res[0]), float(res[1]), float(res[2]))
                te += "{0:20.16f} {1:20.16f} {2:20.16f}\n".format(float(res[0]), float(res[1]), float(res[2]))
    textl += "# bond path information\n" + text_prop
    textl += 'POINTPROP elpot "$4"\n'
    textl += 'POINTPROP lapl "$5"\n'
    textl += "POINT ./POINTS.txt\n"
    lines += "UNLOAD ALL\nEND"

    f = open(fname, 'w')
    print(textl + lines, file=f)
    f.close()

    fname_dir = os.path.dirname(fname)
    f = open(fname_dir + "/POINTS.txt", 'w')
    print(te, file=f)
    f.close()

    f = open(fname_dir + "/POINTSatoms.txt", 'w')
    print(text, file=f)
    f.close()