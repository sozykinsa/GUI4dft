# -*- coding: utf-8 -*-
import os
import math
import sys
from copy import deepcopy

import numpy as np
from utils import helpers
import PySide2.QtCore as QtCore
QtCore.QVariant = "QVariant"
from PySide2.QtGui import QColor, QIcon, QImage, QKeySequence, QPixmap, QStandardItem, QStandardItemModel
from PySide2.QtWidgets import QListWidgetItem, QAction, QApplication, QDialog, QFileDialog, QMessageBox, QColorDialog


sys.path.append('.')

is_with_figure = True



def ase_raman_and_ir_script_create(self):
        if len(self.models) == 0:
            return
        try:
            text = "import numpy as np\n"
            text += "from ase import Atoms\n"
            text += "from ase.calculators.siesta import Siesta\n"
            text += "from ase.calculators.siesta.siesta_lrtddft import RamanCalculatorInterface\n"
            text += "from ase.vibrations.raman import StaticRamanCalculator\n"
            text += "from ase.vibrations.placzek import PlaczekStatic\n"
            text += "from ase.units import Ry, eV, Ha\n"

            model2 = deepcopy(self.models[self.active_model])
            nat = model2.nAtoms()

            formula = model2.formula()

            text += "model = Atoms('" + formula +"', positions=["
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
            mesh = self.FDFData.get_property("MeshCutoff")
            if len(mesh) == 0:
                mesh = "200 Ry"
            mesh = mesh.split()
            text += "mesh_cutoff=" + str(mesh[0]) + " * " + str(mesh[1]) + ",\n"
            basis = self.FDFData.get_property("PAO.BasisSize")
            if len(basis) == 0:
                basis = "DZP"
            text += "basis_set='" + basis + "',\n"
            func = self.FDFData.get_property("XC.functional")
            if len(func) == 0:
                func = "DZP"
            text += "pseudo_qualifier='" + func + "',\n"

            aut = self.FDFData.get_property("XC.authors")
            if len(aut) == 0:
                aut = "PZ"
            text += "xc='" + aut + "',\n"
            shift = self.FDFData.get_property("PAO.EnergyShift")
            if len(shift) == 0:
                shift = "0.03374 Ry"
            shift = shift.split()
            text += "energy_shift=" + str(shift[0]) + " * " + str(shift[1]) + ",\n"
            spin = self.FDFData.get_property("spin")
            if (len(spin) == 0) or (len(spin.split()) > 1):
                spin = "non-polarized"
            text += "spin='" + spin + "',\n"
            kpts = self.FDFData.get_block("kgrid_Monkhorst_Pack")
            kpts = kpts[0].split()[0] + ", " + kpts[1].split()[1] + ", " + kpts[2].split()[2]
            text += "kpts=[" + kpts + "],\n"
            text += "fdf_arguments={\n"
            text += "'SCFMustConverge': False,\n"
            text += "'COOP.Write': True,\n"
            text += "'WriteDenchar': True,\n"
            text += "'PAO.BasisType': 'split',\n"
            split_norm = self.FDFData.get_property("PAO.SplitNorm")
            if (len(split_norm) == 0) or (len(split_norm.split()) > 1):
                split_norm = "0.15"
            text += "'PAO.SplitNorm': " + str(split_norm) + ",\n"
            text += "'DM.Tolerance': 1e-4,\n"
            text += "'MD.NumCGsteps': 0,\n"
            text += "'MD.MaxForceTol': (0.02, 'eV/Ang'),\n"
            text += "'MaxSCFIterations': 10000,\n"
            Pulay = self.FDFData.get_property("DM.NumberPulay")
            if len(Pulay) == 0:
                Pulay = "4"
            text += "'DM.NumberPulay': " + str(Pulay) +",\n"
            Mixing = self.FDFData.get_property("DM.MixingWeight")
            if len(Mixing) == 0:
                Mixing = "0.01"
            text += "'DM.MixingWeight': " + str(Mixing) + ",\n"
            text += "'XML.Write': True,\n"
            text += "'WriteCoorXmol': True,\n"
            text += "'DM.UseSaveDM': True,})\n"

            text += "name = '" + formula + "'\n"
            text += "pynao_args = dict(label='siesta', jcutoff=7, iter_broadening=0.15, xc_code='LDA,PZ', tol_loc=1e-6, tol_biloc=1e-7)\n"
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

            if len(text) > 0:
                name = QFileDialog.getSaveFileName(self, 'Save File', self.work_dir, "Python file (*.py)")[0]
                if len(name) > 0:
                    with open(name, 'w') as f:
                        f.write(text)
        except Exception as e:
            self.show_error(e)


def ase_raman_and_ir_parse(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file', self.work_dir)[0]
            if os.path.exists(fname):
                self.filename = fname
                self.work_dir = os.path.dirname(fname)
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
            for i in range(0, len(raman_inten)):
                raman_text += "{0:10.1f} {1:10.1f} {2:10.2f}\n".format(raman_en_ev[i], raman_en_cm[i], raman_inten[i])
            self.ui.FormRamanSpectraText.setPlainText(raman_text)

            ir_text = "meV cm^-1 Intensity " + units_i + "\n"
            for i in range(0, len(ir_inten)):
                ir_text += "{0:10.1f} {1:10.1f} {2:10.4f}\n".format(ir_en_ev[i], ir_en_cm[i], ir_inten[i])
            self.ui.FormIrSpectraText.setPlainText(ir_text)

        except Exception as e:
            self.show_error(e)


def ase_raman_and_ir_plot(self):
        if self.ui.form_raman_radio.isChecked():
            data = self.ui.FormRamanSpectraText.toPlainText()
            y_title = "Raman"
        else:
            data = self.ui.FormIrSpectraText.toPlainText()
            y_title = "IR"

        col = 1
        x_title = "cm^-1"
        if self.ui.form_spectra_mev_radio.isChecked():
            col = 0
            x_title = "meV"

        x = []
        y = []

        rows = data.split("\n")
        for i in range(1, len(rows)):
            row = rows[i].split()
            if len(row) > 2:
                x.append(float(row[col]))
                y.append(math.log(float(row[2])))

        x_max = max(x)
        n = 1000
        x_fig = np.linspace(0, x_max, n)
        y_fig = np.zeros(n)

        sigma = self.ui.formGaussWidth.value()

        for i in range(0, len(x)):
            for j in range(0, n):
                y_fig[j] += y[i] * math.exp(-math.pow(x[i] - x_fig[j], 2) / ( 2 * sigma) )

        title = "Spectrum"
        self.ui.PyqtGraphWidget.clear()
        self.ui.Form3Dand2DTabs.setCurrentIndex(1)
        self.ui.PyqtGraphWidget.plot([x_fig], [y_fig], [None], title, x_title, y_title, True)
