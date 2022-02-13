# -*- coding: utf-8 -*-

import os
from utils.atomic_model import TAtomicModel
from utils.vasp import TVASP
from utils.fdfdata import TFDFFile
from utils.siesta import TSIESTA
from utils import helpers
import numpy as np
from TInterface import TXSF, TGaussianCube


class Importer(object):

    @staticmethod
    def check_format(filename):
        """check file format"""
        if filename.endswith(".fdf") or filename.endswith(".FDF"):
            return "SIESTAfdf"

        if (filename.lower()).endswith(".out"):
            return "SIESTAout"

        if filename.endswith(".ani") or filename.endswith(".ANI"):
            return "SIESTAANI"

        if (filename.lower()).endswith(".xyz"):
            f = open(filename)
            f.readline()
            str1 = helpers.spacedel(f.readline())
            if len(str1.split()) > 4:
                return "XMolXYZ"
            if len(str1.split()) == 0:
                return "SiestaXYZ"
            return "unknown"

        if filename.endswith(".STRUCT_OUT"):
            return "SIESTASTRUCT_OUT"

        if filename.endswith(".MD_CAR"):
            return "SIESTAMD_CAR"

        if filename.endswith(".XSF"):
            return "SIESTAXSF"

        if filename.endswith(".cube"):
            return "GAUSSIAN_cube"

        if filename.endswith("POSCAR") or filename.endswith("CONTCAR"):
            return "VASPposcar"

        return "unknown"

    @staticmethod
    def Import(filename, fl='all', prop=False, xyzcritic2=False):
        """import file"""
        models = []
        fdf = TFDFFile()
        if os.path.exists(filename):
            fileFormat = Importer.check_format(filename)
            print("File " + str(filename) + " : " + str(fileFormat))

            if fileFormat == "SIESTAfdf":
                models = TAtomicModel.atoms_from_fdf(filename)
                fdf.from_fdf_file(filename)

            if fileFormat == "SIESTAout":
                type_of_run = (TSIESTA.type_of_run(filename).split())[0].lower()
                models = []
                if type_of_run != "sp":
                    if fl != 'opt':
                        models = TAtomicModel.atoms_from_output_cg(filename)
                        if len(models) == 0:
                            models = TAtomicModel.atoms_from_output_md(filename)
                    modelsopt = TAtomicModel.atoms_from_output_optim(filename)
                else:
                    modelsopt = TAtomicModel.atoms_from_output_sp(filename)
                if len(modelsopt) == 1:
                    models.append(modelsopt[0])
                if prop and (len(models) > 0):
                    try:
                        charge_mulliken = TSIESTA.get_charges_mulliken_for_atoms(filename)
                        if len(charge_mulliken[0]) > 0:
                            models[-1].add_atoms_property("charge Mulliken", charge_mulliken)
                        charge_voronoi = TSIESTA.get_charges_voronoi_for_atoms(filename)
                        if len(charge_voronoi[0]) > 0:
                            models[-1].add_atoms_property("charge Voronoi", charge_voronoi)
                        charge_hirshfeld = TSIESTA.get_charges_hirshfeld_for_atoms(filename)
                        if len(charge_hirshfeld[0]) > 0:
                            models[-1].add_atoms_property("charge Hirshfeld", charge_hirshfeld)
                    except Exception:
                        print("Properties failed")
                fdf.from_out_file(filename)

            if fileFormat == "SIESTAANI":
                models = TAtomicModel.atoms_from_ani(filename)

            if fileFormat == "SIESTASTRUCT_OUT":
                models = TAtomicModel.atoms_from_struct_out(filename)

            if fileFormat == "SIESTAMD_CAR":
                models = TAtomicModel.atoms_from_md_car(filename)

            if fileFormat == "SIESTAXSF":
                models = TXSF.get_atoms(filename)

            if fileFormat == "GAUSSIAN_cube":
                models = TGaussianCube.get_atoms(filename)

            if fileFormat == "SiestaXYZ":
                models = TAtomicModel.atoms_from_xyz(filename, xyzcritic2)

            if fileFormat == "XMolXYZ":
                models = TAtomicModel.atoms_from_XMOLxyz(filename)

            if fileFormat == "VASPposcar":
                models = TAtomicModel.atoms_from_POSCAR(filename)
        return models, fdf

    @staticmethod
    def check_dos_file(filename):
        if filename.endswith("DOSCAR"):
            eFermy = TVASP.fermi_energy_from_doscar(filename)
            return filename, eFermy

        """Check DOS file for fdf/out filename"""
        system_label = TSIESTA.SystemLabel(filename)
        file = os.path.dirname(filename) + "/" + str(system_label) + ".DOS"
        if os.path.exists(file):
            return file, TSIESTA.FermiEnergy(filename)
        else:
            return False, 0

    @staticmethod
    def check_cro_file(filename):
        if os.path.exists(filename) and filename.endswith("cro"):
            box_bohr = helpers.from_file_property(filename, "Lattice parameters (bohr):", 1, 'string').split()
            box_bohr = np.array(helpers.list_str_to_float(box_bohr))
            box_ang = helpers.from_file_property(filename, "Lattice parameters (ang):", 1, 'string').split()
            box_ang = np.array(helpers.list_str_to_float(box_ang))
            box_deg = helpers.from_file_property(filename, "Lattice angles (degrees):", 1, 'string').split()
            box_deg = np.array(helpers.list_str_to_float(box_deg))

            MyFile = open(filename)
            str1 = MyFile.readline()
            while str1.find("Critical point list, final report (non-equivalent cps") < 0:
                str1 = MyFile.readline()
            MyFile.readline()
            MyFile.readline()
            MyFile.readline()

            cps = []
            str1 = MyFile.readline()

            while len(str1) > 3:
                str1 = str1.split(')')[1].split()
                x = float(str1[1]) * box_ang[0]
                y = float(str1[2]) * box_ang[1]
                z = float(str1[3]) * box_ang[2]

                line = [str1[0], x, y, z, str1[6], str1[7], str1[8]]
                cps.append(line)
                #print(line)
                str1 = MyFile.readline()

            MyFile.close()
            return box_bohr, box_ang, box_deg, cps
        else:
            return "", "", "", []

    @staticmethod
    def check_pdos_file(filename):
        """Check PDOS file for fdf/out filename"""
        SystemLabel = TSIESTA.SystemLabel(filename)
        file = os.path.dirname(filename) + "/" + str(SystemLabel) + ".PDOS"
        if os.path.exists(file):
            return file
        else:
            return False

    @staticmethod
    def check_bands_file(filename):
        """Check PDOS file for fdf/out filename"""
        SystemLabel = TSIESTA.SystemLabel(filename)
        file = os.path.dirname(filename) + "/" + str(SystemLabel) + ".bands"
        if os.path.exists(file):
            return file
        else:
            return False
