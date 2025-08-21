import os

import numpy as np

from core_atomistic.project_file import ProjectFile
from src_critplot.models.cp import CriticalPoint
from src_critplot.models.cp_model import AtomicModelCP


class CritPlotProjectFile(ProjectFile):

    @staticmethod
    def project_file_writer(model):
        text = ProjectFile.project_file_writer(model)
        try:
            cps = model.cps
            text += "%critical points\n"
            for point in cps:
                text += point.to_string() + point.properties_to_string() + "\n"  # point.bonds_to_string() + "\n"
            text += "%end critical points\n"
        except:
            pass

        return text

    @staticmethod
    def project_file_reader(file_name):
        model = None
        if os.path.exists(file_name):
            atomic_model = ProjectFile.project_file_reader(file_name)
            model = AtomicModelCP()
            model.atoms = atomic_model[0].atoms
            model.lat_vectors = atomic_model[0].lat_vectors
            f = open(file_name)
            row = f.readline()
            while row:
                if row.find("%critical points") >= 0:
                    row = f.readline()
                    while row.find("%end critical points") < 0:
                        coords = row.split("properties:")[0]
                        props = row.split("properties:")
                        row = coords.split()
                        if row[0] == "xb":
                            let = "xb"
                            x = float(row[1])
                            y = float(row[2])
                            z = float(row[3])
                            charge = -1
                            xyz = np.array([x, y, z])
                            new_cp = CriticalPoint([xyz, let, charge])
                            if len(props) > 1:
                                new_cp.properties_from_string(props[1])
                            model.add_critical_point(new_cp)
                        row = f.readline()
                row = f.readline()
            f.close()

            for cp in model.cps:
                ind1 = cp.get_property("atom1")
                ind2 = cp.get_property("atom2")
                if (ind1 is not None) and (ind2 is not None):
                    trans1 = np.array(cp.get_property("atom1_translation"))
                    trans2 = np.array(cp.get_property("atom2_translation"))
                    p1 = CriticalPoint([model.atoms[ind1 - 1].xyz + trans1, "xz", "bp"])
                    p2 = CriticalPoint([cp.xyz, "xz", "bp"])
                    p3 = CriticalPoint([model.atoms[ind2 - 1].xyz + trans2, "xz", "bp"])
                    model.add_bond_path_point([p2, p1])
                    model.add_bond_path_point([p2, p3])
                    atom_to_atom = model.atoms[ind1 - 1].let + str(ind1) + "-" + model.atoms[ind2 - 1].let + str(ind2)
                    cp.set_property("atom_to_atom", atom_to_atom)
                    bond_len = np.linalg.norm(model.atoms[ind2 - 1].xyz + trans2 - model.atoms[ind1 - 1].xyz - trans1)
                    cp.set_property("cp_bp_len", bond_len)
            model.bond_path_points_optimize()
        return model
