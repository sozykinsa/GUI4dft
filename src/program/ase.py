# -*- coding: utf-8 -*-
import numpy as np

from src_core_atomistic import helpers
from src_core_atomistic.atom import Atom
from src_core_atomistic.atomic_model import AtomicModel
from src_core_atomistic.periodic_table import TPeriodTable


def from_ase_atoms_to_atomic_model(ase_atoms):
    model = AtomicModel()
    positions = ase_atoms.get_positions()
    atomic_numbers = ase_atoms.get_atomic_numbers()
    mendeley = TPeriodTable()
    letters = mendeley.get_all_letters()
    for pos, numb in zip(positions, atomic_numbers):
        model.add_atom(Atom([*pos, letters[numb], numb]))
    cell = ase_atoms.cell
    model_cell = np.eye(3, dtype=float)
    # print(cell, cell[0][0], cell[0][1], cell[0][2])
    if cell[0].size == 3:
        model_cell[0][0] = cell[0][0]
        model_cell[1][1] = cell[1][1]
        model_cell[2][2] = cell[2][2]
        # print(model_cell)
        model.lat_vectors = model_cell
    return model


def ase_raman_and_ir_script_create(model2, FDFData):
    text = "import numpy as np\n"
    text += "from ase import Atoms\n"
    text += "from ase.calculators.siesta import Siesta\n"
    text += "from ase.calculators.siesta.siesta_lrtddft import RamanCalculatorInterface\n"
    text += "from ase.vibrations.raman import StaticRamanCalculator\n"
    text += "from ase.vibrations.placzek import PlaczekStatic\n"
    text += "from ase.units import Ry, eV, Ha\n"

    nat = model2.n_atoms()

    formula = model2.formula()

    text += "model = Atoms('" + formula + "', positions=["
    for i in range(0, nat):
        x = str(model2.atoms[i].x)
        y = str(model2.atoms[i].y)
        z = str(model2.atoms[i].z)
        text += "(" + x + ",   " + y + ",   " + z + "),\n"
    text += "], cell=["
    text += str(model2.get_LatVect1_norm()) + ", "
    text += str(model2.get_LatVect2_norm()) + ", "
    text += str(model2.get_LatVect3_norm()) + "])\n"

    text += "model.center(about=(0., 0., 0.))\n"

    text += "# set-up the Siesta parameters\n"
    text += "model.calc = Siesta(\n"
    mesh = FDFData.get_property("MeshCutoff")
    if len(mesh) == 0:
        mesh = "200 Ry"
    mesh = mesh.split()
    text += "mesh_cutoff=" + str(mesh[0]) + " * " + str(mesh[1]) + ",\n"
    basis = FDFData.get_property("PAO.BasisSize")
    if len(basis) == 0:
        basis = "DZP"
    text += "basis_set='" + basis + "',\n"
    func = FDFData.get_property("XC.functional")
    if len(func) == 0:
        func = "DZP"
    text += "pseudo_qualifier='" + func + "',\n"

    aut = FDFData.get_property("XC.authors")
    if len(aut) == 0:
        aut = "PZ"
    text += "xc='" + aut + "',\n"
    shift = FDFData.get_property("PAO.EnergyShift")
    if len(shift) == 0:
        shift = "0.03374 Ry"
    shift = shift.split()
    text += "energy_shift=" + str(shift[0]) + " * " + str(shift[1]) + ",\n"
    spin = FDFData.get_property("spin")
    if (len(spin) == 0) or (len(spin.split()) > 1):
        spin = "non-polarized"
    text += "spin='" + spin + "',\n"
    kpts = FDFData.get_block("kgrid_Monkhorst_Pack")
    kpts = kpts[0].split()[0] + ", " + kpts[1].split()[1] + ", " + kpts[2].split()[2]
    text += "kpts=[" + kpts + "],\n"
    text += "fdf_arguments={\n"
    text += "'SCFMustConverge': False,\n"
    text += "'COOP.Write': True,\n"
    text += "'WriteDenchar': True,\n"
    text += "'PAO.BasisType': 'split',\n"
    split_norm = FDFData.get_property("PAO.SplitNorm")
    if (len(split_norm) == 0) or (len(split_norm.split()) > 1):
        split_norm = "0.15"
    text += "'PAO.SplitNorm': " + str(split_norm) + ",\n"
    text += "'DM.Tolerance': 1e-4,\n"
    text += "'MD.NumCGsteps': 0,\n"
    text += "'MD.MaxForceTol': (0.02, 'eV/Ang'),\n"
    text += "'MaxSCFIterations': 10000,\n"
    Pulay = FDFData.get_property("DM.NumberPulay")
    if len(Pulay) == 0:
        Pulay = "4"
    text += "'DM.NumberPulay': " + str(Pulay) + ",\n"
    Mixing = FDFData.get_property("DM.MixingWeight")
    if len(Mixing) == 0:
        Mixing = "0.01"
    text += "'DM.MixingWeight': " + str(Mixing) + ",\n"
    text += "'XML.Write': True,\n"
    text += "'WriteCoorXmol': True,\n"
    text += "'DM.UseSaveDM': True,})\n"

    text += "name = '" + formula + "'\n"
    text += "pynao_args = dict(label='siesta', jcutoff=7, iter_broadening=0.15, "
    text += "xc_code='LDA,PZ', tol_loc=1e-6, tol_biloc=1e-7)\n"
    text += "rm = StaticRamanCalculator(model, RamanCalculatorInterface, name=name, delta=0.011, exkwargs=pynao_args)\n"
    text += "# save dipole moments from DFT calculation in order to get\n"
    text += "# infrared intensities as well\n"
    text += "rm.ir = True\n"
    text += "rm.run()\n"
    text += "pz = PlaczekStatic(model, name=name)\n"
    text += "e_vib = pz.get_energies()\n"
    text += "pz.summary()\n"

    text += "from ase.vibrations.infrared import Infrared\n"
    text += "# finite displacement for vibrations\n"
    text += "ir = Infrared(model, name=name)\n"
    text += "ir.run()\n"
    text += "ir.summary()\n"
    return text


def ase_raman_and_ir_parse(fname):
    f = open(fname)
    rows = f.readlines()

    is_raman = False
    is_ir = False

    raman_en_ev = []
    raman_en_cm = []
    raman_inten = []

    ir_en_ev = []
    ir_en_cm = []
    ir_inten = []

    i = 0

    units_r = ""
    units_i = ""
    while i < len(rows):
        if rows[i].find("A^4/amu") >= 0:
            is_raman = True
            units_r = rows[i].split("cm^-1")[1]
            i += 2

        if rows[i].find(")^2 amu^-1") >= 0:
            is_ir = True
            units_i = rows[i].split("cm^-1")[1]
            i += 2

        if rows[i].find("---------------------") >= 0:
            is_raman = False
            is_ir = False
            i += 1

        if len(rows[i].split()) == 4:
            row = rows[i].split()
            if (row[0]).isdigit() and helpers.is_number(row[1]):
                if (float(row[1]) > 0) and (float(row[3]) > 0):
                    if is_raman:
                        raman_en_ev.append(float(row[1]))
                        raman_en_cm.append(float(row[2]))
                        raman_inten.append(float(row[3]))

                    if is_ir:
                        ir_en_ev.append(float(row[1]))
                        ir_en_cm.append(float(row[2]))
                        ir_inten.append(float(row[3]))
        i += 1
    raman_text = "meV cm^-1 Intensity " + units_r + "\n"
    return raman_text, units_i, raman_inten, raman_en_ev, raman_en_cm, ir_inten, ir_en_ev, ir_en_cm
