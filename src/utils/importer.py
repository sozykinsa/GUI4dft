# -*- coding: utf-8 -*-

import os
from models.atomic_model import TAtomicModel
from thirdparty.vasp import fermi_energy_from_doscar, atoms_from_POSCAR
from utils.fdfdata import TFDFFile
from utils.siesta import TSIESTA
from utils import helpers
from models.gaussiancube import GaussianCube
from models.xsf import XSF


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
    def import_from_file(filename, fl='all', prop=False, xyzcritic2=False):
        """import file"""
        models = []
        fdf = TFDFFile()
        if os.path.exists(filename):
            file_format = Importer.check_format(filename)
            print("File " + str(filename) + " : " + str(file_format))

            if file_format == "SIESTAfdf":
                models = TAtomicModel.atoms_from_fdf(filename)
                fdf.from_fdf_file(filename)

            if file_format == "SIESTAout":
                models = Importer.get_output_data(filename, fl, models, prop)
                fdf.from_out_file(filename)

            if file_format == "SIESTAANI":
                models = TAtomicModel.atoms_from_ani(filename)

            if file_format == "SIESTASTRUCT_OUT":
                models = TAtomicModel.atoms_from_struct_out(filename)

            if file_format == "SIESTAMD_CAR":
                models = TAtomicModel.atoms_from_md_car(filename)

            if file_format == "SIESTAXSF":
                models = XSF.get_atoms(filename)

            if file_format == "GAUSSIAN_cube":
                models = GaussianCube.get_atoms(filename)

            if file_format == "SiestaXYZ":
                models = TAtomicModel.atoms_from_xyz(filename, xyzcritic2)

            if file_format == "XMolXYZ":
                models = TAtomicModel.atoms_from_xmol_xyz(filename)

            if file_format == "VASPposcar":
                models = atoms_from_POSCAR(filename)
        return models, fdf

    @staticmethod
    def get_output_data(filename, fl, models, prop):
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
        return models

    @staticmethod
    def check_dos_file(filename):
        """Check DOS file for fdf/out filename."""
        if filename.endswith("DOSCAR"):
            return filename, fermi_energy_from_doscar(filename)

        system_label = TSIESTA.system_label(filename)
        file = os.path.dirname(filename) + "/" + str(system_label) + ".DOS"
        if os.path.exists(file):
            return file, TSIESTA.FermiEnergy(filename)
        else:
            return False, 0

    @staticmethod
    def check_pdos_file(filename):
        """Check PDOS file for fdf/out filename."""
        system_label = TSIESTA.system_label(filename)
        file = os.path.dirname(filename) + "/" + str(system_label) + ".PDOS"
        if os.path.exists(file):
            return file
        else:
            return False

    @staticmethod
    def check_bands_file(filename):
        """Check PDOS file for fdf/out filename."""
        system_label = TSIESTA.system_label(filename)
        file = os.path.dirname(filename) + "/" + str(system_label) + ".bands"
        if os.path.exists(file):
            return file
        else:
            return False
