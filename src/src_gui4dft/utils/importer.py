# -*- coding: utf-8 -*-

import os
from core_gui_atomistic.atomic_model import AtomicModel
from src_gui4dft.program.vasp import fermi_energy_from_doscar, atoms_from_POSCAR
from src_gui4dft.utils.fdfdata import TFDFFile
from src_gui4dft.program.siesta import TSIESTA
from core_gui_atomistic import helpers
from core_gui_atomistic.gui4dft_project_file import GUI4dftProjectFile
from src_gui4dft.models.gaussiancube import GaussianCube
from src_gui4dft.models.xsf import XSF


class Importer(object):
    @staticmethod
    def import_from_file(filename, fl='all', prop=False):
        """import file"""
        models = []
        fdf = TFDFFile()
        if os.path.exists(filename):
            file_format = helpers.check_format(filename)
            print("File " + str(filename) + " : " + str(file_format))

            if file_format == "SIESTAfdf":
                models = TSIESTA.atoms_from_fdf(filename)
                fdf.from_fdf_file(filename)

            elif file_format == "SIESTAout":
                models = TSIESTA.get_output_data(filename, fl, models, prop)
                fdf.from_out_file(filename)

            elif file_format == "SIESTAANI":
                models = TSIESTA.atoms_from_ani(filename)

            elif file_format == "SIESTASTRUCT_OUT":
                models = TSIESTA.atoms_from_struct_out(filename)

            elif file_format == "SIESTAMD_CAR":
                models = TSIESTA.atoms_from_md_car(filename)

            elif file_format == "SIESTAXSF":
                models = XSF.get_atoms(filename)

            elif file_format == "GAUSSIAN_cube":
                models = GaussianCube.get_atoms(filename)

            elif file_format == "SiestaXYZ":
                models = AtomicModel.atoms_from_xyz(filename)

            elif file_format == "XMolXYZ":
                models = AtomicModel.atoms_from_xmol_xyz(filename)

            elif file_format == "VASPposcar":
                models = atoms_from_POSCAR(filename)
            elif file_format == "project":
                models = GUI4dftProjectFile.project_file_reader(filename)
            else:
                print("Wrong format")

        return models, fdf

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
