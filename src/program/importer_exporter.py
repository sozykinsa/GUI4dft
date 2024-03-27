# -*- coding: utf-8 -*-

import os
from core_atomistic.atomic_model import AtomicModel
from core_atomistic import helpers
from core_atomistic.project_file import ProjectFile
from program.fdfdata import TFDFFile
from program.siesta import TSIESTA
from program.firefly import atomic_model_to_firefly_inp
from program.crystal import structure_of_primitive_cell, structure_opt_step
from program.qe import atoms_from_pwout
from program.dftb import atoms_from_gen
from program.lammps import atoms_trajectory_step
from program.vasp import fermi_energy_from_doscar, atoms_from_poscar, atoms_from_outcar, model_to_vasp_poscar
from program.wien import atoms_from_struct
from program.gaussiancube import GaussianCube
from program.xsf import XSF


class ImporterExporter(object):
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

            elif file_format == "siesta_out":
                models = TSIESTA.get_output_data(filename, fl, models, prop)
                if len(models) == 0:
                    models = TSIESTA.atoms_from_fdf(filename)
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
                models = atoms_from_poscar(filename)

            elif file_format == "vasp_outcar":
                models = atoms_from_outcar(filename)

            elif file_format == "CRYSTALout":
                models = structure_of_primitive_cell(filename)

            elif (file_format == "CRYSTALopt_cryst") or (file_format == "CRYSTALopt_atom"):
                models = structure_opt_step(filename)

            elif file_format == "QEPWout":
                models = atoms_from_pwout(filename)

            elif file_format == "WIENstruct":
                models = atoms_from_struct(filename)

            elif file_format == "DFTBgen":
                models = atoms_from_gen(filename)

            elif file_format == "LammpsTrj":
                models = atoms_trajectory_step(filename)

            elif file_format == "project":
                models = ProjectFile.project_file_reader(filename)
            else:
                print("Wrong format")

        return models, fdf

    @staticmethod
    def export_to_file(model, f_name):  # pragma: no cover
        text = ""
        if f_name.find("POSCAR") >= 0:
            f_name = f_name.split(".")[0]
            text = model_to_vasp_poscar(model)
        if f_name.endswith(".inp"):
            text = atomic_model_to_firefly_inp(model)
        if f_name.endswith(".fdf"):
            text = TSIESTA.to_siesta_fdf_data(model, "Fractional", "Ang", "LatticeVectors")
        if f_name.endswith(".xyz"):
            text = TSIESTA.to_siesta_xyz_data(model)
        if f_name.endswith(".data"):
            text = ProjectFile.project_file_writer(model)
        helpers.write_text_to_file(f_name, text)

    @staticmethod
    def check_dos_file(filename):
        """Check DOS file for fdf/out filename."""
        if filename.endswith("DOSCAR"):
            return filename, fermi_energy_from_doscar(filename)

        system_label = TSIESTA.system_label(filename)
        file = os.path.dirname(filename) + "/" + str(system_label) + ".DOS"
        if os.path.exists(file):
            return file, TSIESTA.fermi_energy(filename)
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
