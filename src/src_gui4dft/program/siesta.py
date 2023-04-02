# -*- coding: utf-8 -*-
import os
import re

import numpy as np

from core_gui_atomistic import helpers
import xml.etree.ElementTree as ET
from core_gui_atomistic.periodic_table import TPeriodTable
from core_gui_atomistic.atom import Atom
from core_gui_atomistic.atomic_model import AtomicModel
from core_gui_atomistic.helpers import clear_fdf_lines, text_between_lines


class TSIESTA:

    @staticmethod
    def lattice_constant(filename):
        """Returns the LatticeConstant from SIESTA output file."""
        mult = 1
        latc = helpers.from_file_property(filename, 'LatticeConstant', 1, 'unformatted')
        if latc is None:
            return 1
        prop = latc.split()
        if prop[1].lower() == "bohr":
            mult = 0.52917720859
        return mult * float(prop[0])

    @staticmethod
    def lattice_parameters_abc_angles(filename):
        """Returns data from LatticeParameters block of file."""
        lattice_parameters = TSIESTA.get_block_from_siesta_fdf(filename, 'LatticeParameters')
        lat_constant = float(TSIESTA.lattice_constant(filename))
        return helpers.lattice_parameters_abc_angles(lattice_parameters, lat_constant)

    @staticmethod
    def lattice_vectors(filename):
        lat_constant = float(TSIESTA.lattice_constant(filename))
        lattice_vectors = TSIESTA.get_block_from_siesta_fdf(filename, 'LatticeVectors')
        lat_vectors = np.zeros((3, 3), dtype=float)
        if len(lattice_vectors) > 0:
            lat_vect_1 = helpers.spacedel(lattice_vectors[0]).split()
            lat_vectors[0] = np.array(helpers.list_str_to_float(lat_vect_1))
            lat_vect_2 = helpers.spacedel(lattice_vectors[1]).split()
            lat_vectors[1] = np.array(helpers.list_str_to_float(lat_vect_2))
            lat_vect_3 = helpers.spacedel(lattice_vectors[2]).split()
            lat_vectors[2] = np.array(helpers.list_str_to_float(lat_vect_3))
            return lat_constant * lat_vectors
        return None

    @staticmethod
    def calc_pdos(file, atom_index, species, number_l, number_m, number_n, number_z):
        tree = ET.parse(file)
        root = tree.getroot()
        pdos = np.zeros((2, 1000))
        energy = np.zeros((1, 10))
        nspin = 1
        for child in root:
            if child.tag == "nspin":
                nspin = int(child.text)
            if child.tag == "energy_values":
                data = child.text.split()
                data = helpers.list_str_to_float(data)
                energy = np.array(data)
                pdos = np.zeros((nspin, len(energy)))

            if child.tag == "orbital":
                if (int(child.attrib['atom_index']) in atom_index) and (child.attrib['species'] in species) and (
                        int(child.attrib['n']) in number_n) and (int(child.attrib['l']) in number_l) and (
                        int(child.attrib['m']) in number_m) and (int(child.attrib['z']) in number_z):
                    for children in child:
                        data = children.text.split()
                        data = helpers.list_str_to_float(data)
                        data = np.array(data)
                        data = data.reshape((nspin, len(energy)), order='F')
                        pdos += data
        return pdos, energy

    @staticmethod
    def get_charges_for_atoms(filename, method):
        if os.path.exists(filename):
            number_of_atoms = TSIESTA.number_of_atoms(filename)
            charges = []
            for i in range(0, number_of_atoms):
                charges.append([])

            if method == "Mulliken":
                charges = TSIESTA.get_charge_mulliken(charges, filename, number_of_atoms)
                return charges

            search_str1 = ""
            search_str2 = ""
            if method == "Hirshfeld":
                search_str1 = "Hirshfeld Net Atomic Populations:"
                search_str2 = "Hirshfeld Atomic Populations:"

            if method == "Voronoi":
                search_str1 = "Voronoi Net Atomic Populations:"
                search_str2 = "Voronoi Atomic Populations:"

            md_siesta_file = open(filename)
            str1 = md_siesta_file.readline()
            mendeley = TPeriodTable()

            while str1 != '':
                if str1 != '' and ((str1.find(search_str1) >= 0) or (str1.find(search_str2) >= 0)):
                    md_siesta_file.readline()
                    for i in range(0, number_of_atoms):
                        data = (helpers.spacedel(md_siesta_file.readline())).split(' ')
                        charge = float(data[1])
                        atom_sort = mendeley.get_charge_by_letter(data[-1])
                        charges[i] = [atom_sort, charge]
                str1 = md_siesta_file.readline()
            md_siesta_file.close()
        return charges

    @staticmethod
    def get_charge_mulliken(charges, filename, number_of_atoms):
        pseudo_charges = TSIESTA.pseudo_charge_of_species(filename)
        number_of_species = len(pseudo_charges)
        species = TSIESTA.get_species(filename)
        is_spin_polarized = int(helpers.from_file_property(filename, 'redata: Number of spin components', 1,
                                                           'string').split("=")[1])
        md_siesta_file = open(filename)
        str1 = md_siesta_file.readline()
        if is_spin_polarized == 2:
            number_of_species *= 2
            number_of_atoms *= 2
        charges_for_all_steps = []
        while str1 != '':
            if str1 != '' and (str1.find("mulliken: Atomic and Orbital Populations:") >= 0):
                nsp = 0

                charges_m = []
                for i in range(0, len(charges)):
                    charges_m.append(["", 0])

                while nsp < number_of_species:
                    atoms = 0
                    atom_sort = -1
                    while str1.find("mulliken:") >= 0 or len(str1) < 2 or str1.find("Species:") >= 0:
                        if str1.find("Species:") >= 0:
                            str1 = helpers.spacedel(str1)
                            nsp += 1
                            for i in range(0, len(species)):
                                if str1.split(' ')[1] == species[i][2]:
                                    atom_sort = i
                        str1 = md_siesta_file.readline()
                    neutral = pseudo_charges[atom_sort]
                    if is_spin_polarized == 2:
                        neutral /= 2.0

                    skip = 0
                    str1 = helpers.spacedel(md_siesta_file.readline())
                    while not helpers.is_integer(str1.split()[0]):
                        str1 = helpers.spacedel(md_siesta_file.readline())
                        if len(str1) == 0:
                            str1 = helpers.spacedel(md_siesta_file.readline())
                        skip += 1

                    while str1 != '\n':
                        if str1 != '\n':
                            atoms += 1
                            str1 = helpers.spacedel(str1)
                            at = int(str1.split(' ')[0])
                            chr = float(str1.split(' ')[1])
                            charges_m[at - 1][0] = species[atom_sort][1]
                            charges_m[at - 1][1] += neutral - chr
                        for i in range(0, skip):
                            str1 = md_siesta_file.readline()

                charges_for_all_steps.append(charges_m)
            str1 = md_siesta_file.readline()
        md_siesta_file.close()
        if len(charges_for_all_steps) > 0:
            charges = charges_for_all_steps[-1]
            for i in range(0, len(charges)):
                charges[i][1] = round(charges[i][1], 3)
        return charges

    @staticmethod
    def get_charges_voronoi_for_atoms(filename):
        return TSIESTA.get_charges_for_atoms(filename, "Voronoi")

    @staticmethod
    def get_charges_hirshfeld_for_atoms(filename):
        return TSIESTA.get_charges_for_atoms(filename, "Hirshfeld")

    @staticmethod
    def get_charges_mulliken_for_atoms(filename):
        return TSIESTA.get_charges_for_atoms(filename, "Mulliken")

    @staticmethod
    def energy_tot(filename):
        """ Returns the Etot from SIESTA output file """
        if os.path.exists(filename):
            return helpers.from_file_property(filename, 'siesta: Etot    =', 2, 'float')
        else:
            return None

    @staticmethod
    def energies(filename):
        """Energy from each step."""
        return TSIESTA.list_of_values(filename, "siesta: E_KS(eV) =")

    @staticmethod
    def FermiEnergy(filename):
        """ Fermy Energy from SIESTA output file """
        if os.path.exists(filename):
            energy = 0
            try:
                energy = float(helpers.from_file_property(filename, 'siesta:         Fermi =', 2, 'float'))
            except Exception:
                md_siesta_file = open(filename)
                str1 = md_siesta_file.readline()
                energy_string = "0 0 0 0 0 0 0"
                search1 = "siesta: iscf   Eharris(eV)      E_KS(eV)   FreeEng(eV)   dDmax  Ef(eV)"
                search2 = "scf: iscf   Eharris(eV)      E_KS(eV)   FreeEng(eV)    dDmax  Ef(eV)"
                search3 = "iscf     Eharris(eV)        E_KS(eV)     FreeEng(eV)     dDmax    Ef(eV) dHmax(eV)"
                while str1 != '':
                    if str1 != '' and (str1.find(search1) >= 0) or (str1.find(search2) >= 0) or \
                            (str1.find(search3) >= 0):
                        str1 = md_siesta_file.readline()
                        while (str1.find('siesta') >= 0) or (str1.find('timer') >= 0) or (str1.find('elaps') >= 0) or (
                                str1.find('scf:') >= 0) or (str1.find('spin moment:') >= 0):
                            str1 = helpers.spacedel(str1)
                            if (str1.find('siesta') >= 0) or (str1.find('scf:') >= 0):
                                energy_string = str1
                            str1 = md_siesta_file.readline()
                    str1 = md_siesta_file.readline()
                md_siesta_file.close()
                energy = float(energy_string.split(' ')[6])
            return energy
        else:
            return None

    @staticmethod
    def number_of_atoms(filename):
        """Returns the NumberOfAtoms from SIESTA output file."""
        number = helpers.from_file_property(filename, 'NumberOfAtoms')
        if number is None:
            block = TSIESTA.get_block_from_siesta_fdf(filename, "AtomicCoordinatesAndAtomicSpecies")
            if len(block) > 0:
                return len(block)
        return number

    @staticmethod
    def number_of_species(filename):
        """ Returns the NumberOfSpecies from SIESTA output file """
        return helpers.from_file_property(filename, 'NumberOfSpecies')

    @staticmethod
    def atoms_from_fdf(filename):
        """Return a AtList from fdf file."""
        atomic_coord_format, n_atoms, chem_spec_info, lat, lat_vectors, units = TSIESTA.atoms_from_fdf_prepare(filename)
        f = open(filename)
        lines = f.readlines()
        f.close()
        all_atoms = TSIESTA.atoms_from_fdf_text(atomic_coord_format, n_atoms, chem_spec_info, lat, lat_vectors, lines,
                                                units)
        return [all_atoms]

    @staticmethod
    def pseudo_charge_of_species(filename):
        """ Returns the pseudo charge from SIESTA output file (from pseudopotential file) """
        species = TSIESTA.get_species(filename)
        siesta_file = open(filename)
        str1 = siesta_file.readline()
        pseudo_charges = []

        while str1 != '':
            if str1 != '' and (str1.find("initatom: Reading input for the pseudopotentials and atomic orbitals") >= 0):
                for i in range(0, len(species) + 1):
                    str1 = siesta_file.readline()
                for j in range(0, len(species)):
                    pseudo_charges.append(0)
                    while str1.find("Ground state valence configuration:") < 0:
                        str1 = siesta_file.readline()
                    states = (helpers.spacedel(str1.split(":")[1])).split(" ")
                    n_states = len(states)
                    while str1.find("Valence configuration for ps") < 0:
                        str1 = siesta_file.readline()
                    for i in range(0, n_states):
                        str1 = siesta_file.readline()
                        pseudo_charges[j] += float((str1.split("(")[1]).split(")")[0])
                return pseudo_charges
            str1 = siesta_file.readline()
        return pseudo_charges

    @staticmethod
    def atomic_coordinates_format(filename):
        """Returns the AtomicCoordinatesFormat from SIESTA output file."""
        format = helpers.from_file_property(filename, 'AtomicCoordinatesFormat', 1, 'string')
        if format is None:
            formatlow = ""
        else:
            formatlow = format.lower()
        ans = "NotScaledCartesianBohr"
        if (formatlow == "ang") or (formatlow == "notscaledcartesianang"):
            ans = "NotScaledCartesianAng"
        if (formatlow == "fractional") or (formatlow == "scaledbylatticevectors"):
            ans = "ScaledByLatticeVectors"
        if formatlow == "scaledcartesian":
            ans = "ScaledCartesian"
        return ans

    @staticmethod
    def get_species(filename):
        """Returns the LIST of Speciecies from SIESTA output or fdf file."""
        species = []
        if os.path.exists(filename):
            number_of_species = TSIESTA.number_of_species(filename)
            md_siesta_file = open(filename)
            str1 = md_siesta_file.readline()
            while str1 != '':
                if str1 != '' and (str1.find("block ChemicalSpeciesLabel") >= 0):
                    str1 = md_siesta_file.readline()
                    for i in range(0, number_of_species):
                        row = helpers.spacedel(str1).split(' ')[:3]
                        row[0] = int(row[0])
                        row[1] = int(row[1])
                        species.append(row)
                        str1 = md_siesta_file.readline()
                    species.sort(key=lambda line: line[0])
                    return species
                str1 = md_siesta_file.readline()
        species.sort(key=lambda line: line[0])
        return species

    @staticmethod
    def system_label(filename):
        """Returns the SystemLabel SIESTA output file."""
        res = helpers.from_file_property(filename, 'SystemLabel', 1, "string")
        if res is None:
            res = "siesta"
        return res

    @staticmethod
    def spin_polarized(filename):
        """Returns the SpinPolarized from SIESTA output file."""
        res = helpers.from_file_property(filename, 'Spin', prop_type='string')
        if res is None:
            res = helpers.from_file_property(filename, 'SpinPolarized', prop_type='string')
            if res is None:
                res = False
        else:
            if res == "non-polarized":
                res = False
        return res

    @staticmethod
    def list_of_values(filename, prop):
        """Return all float values of prop from filename."""
        list_of_val = []
        if os.path.exists(filename):
            f = open(filename)
            for st in f:
                if st.find(prop) >= 0:
                    list_of_val.append(float(re.findall(r"[0-9,\.,-]+", st)[0]))
            f.close()
        return list_of_val

    @staticmethod
    def get_block_from_siesta_fdf(filename, blockname):
        """ возвращает содержимое блока входного файла """
        lines = []
        flag = 0
        f = open(filename)
        blockname = blockname.lower()
        for line in f:
            line1 = line.lower()
            if (line1.find(blockname) < 0) and (flag == 1):
                lines.append(line)
            if (line1.find(blockname) >= 0) and (flag == 1):
                f.close()
                return lines
            if (line1.find(blockname) >= 0) and (flag == 0):
                flag = 1
        return []

    @staticmethod
    def type_of_run(filename):
        steps = helpers.from_file_property(filename, 'MD.NumCGsteps', 1, 'int')
        if steps == 0:
            """ single point """
            return "sp"
        """ MD or CG? """
        res = helpers.from_file_property(filename, 'MD.TypeOfRun', 1, 'string')
        if res is None:
            res = helpers.from_file_property(filename, "Begin CG opt. move =", 1, 'string')
            if res == "0":
                return "cg"
            res = helpers.from_file_property(filename, "Begin MD step =", 1, 'string')
            if res == "1":
                return "mg"
            res = "cg"
        return res

    @staticmethod
    def volume(filename):
        """Returns cell volume from SIESTA output file."""
        if os.path.exists(filename):
            return helpers.from_file_property(filename, 'siesta: Cell volume = ', 1, 'float')
        else:
            return None

    @staticmethod
    def model_to_siesta_xyz_data(model: AtomicModel):
        """Returns data for *.xyz file."""
        data = "  "
        n_atoms = model.n_atoms()
        data += str(n_atoms) + "\n"
        for i in range(0, n_atoms):
            data += "\n" + model.atoms[i].let + '       ' + model.xyz_string(i)
        return data

    @staticmethod
    def to_siesta_fdf_data(model, coord_style, units_type, latt_style='LatticeParameters'):
        """Returns data for SIESTA fdf file."""
        data = ""
        periodic_table = TPeriodTable()
        data += 'NumberOfAtoms ' + str(len(model.atoms)) + "\n"
        types = model.types_of_atoms()
        data += 'NumberOfSpecies ' + str(len(types)) + "\n"
        data += "WriteCoorStep True\n"
        data += '%block ChemicalSpeciesLabel\n'
        for i in range(0, len(types)):
            data += ' ' + str(i + 1) + '  ' + str(types[i][0]) + '  ' +\
                    str(periodic_table.get_let(int(types[i][0]))) + "\n"
        data += '%endblock ChemicalSpeciesLabel\n'

        mult = 1
        lattice_constant = 'LatticeConstant       1.0 Ang\n'

        if (coord_style != "Zmatrix Cartesian") and (units_type == "Bohr"):
            mult = 1.0 / 0.52917720859
            lattice_constant = 'LatticeConstant       1.0 Bohr\n'

        data += lattice_constant

        if latt_style == 'LatticeParameters':
            data += '%block LatticeParameters\n'
            data += '  ' + str(np.linalg.norm(model.lat_vector1) * mult) + '  ' + \
                    str(np.linalg.norm(model.lat_vector2) * mult) + '  ' + \
                    str(np.linalg.norm(model.lat_vector3) * mult) + '  ' + str(model.get_angle_alpha()) + '  ' + \
                    str(model.get_angle_beta()) + '  ' + str(model.get_angle_gamma()) + '\n'
            data += '%endblock LatticeParameters\n'
        # or
        if latt_style == 'LatticeVectors':
            data += '%block LatticeVectors\n'
            data += '  ' + str(model.lat_vector1[0] * mult) + '  ' + str(model.lat_vector1[1] * mult) + '  ' + str(
                model.lat_vector1[2] * mult) + '\n'
            data += '  ' + str(model.lat_vector2[0] * mult) + '  ' + str(model.lat_vector2[1] * mult) + '  ' + str(
                model.lat_vector2[2] * mult) + '\n'
            data += '  ' + str(model.lat_vector3[0] * mult) + '  ' + str(model.lat_vector3[1] * mult) + '  ' + str(
                model.lat_vector3[2] * mult) + '\n'
            data += '%endblock LatticeVectors\n'

        if coord_style == "Zmatrix Cartesian":
            data += 'AtomicCoordinatesFormat NotScaledCartesianAng\n'
            data += "ZM.UnitsLength Ang\n"
            data += '%block Zmatrix\n'
            data += 'cartesian\n'
            data += model.coords_for_export(coord_style)
            data += '%endblock Zmatrix\n'

        if coord_style == "Fractional":
            model.sort_atoms_by_type()
            model.go_to_positive_coordinates()
            model.convert_from_cart_to_direct()
            data += 'AtomicCoordinatesFormat Fractional\n'
            data += '%block AtomicCoordinatesAndAtomicSpecies\n'
            data += model.coords_for_export(coord_style)
            data += '%endblock AtomicCoordinatesAndAtomicSpecies\n'

        if coord_style == "Cartesian":
            model.sort_atoms_by_type()
            data += 'AtomicCoordinatesFormat ' + units_type + '\n'
            data += '%block AtomicCoordinatesAndAtomicSpecies\n'
            data += model.coords_for_export(coord_style, units_type)
            data += '%endblock AtomicCoordinatesAndAtomicSpecies\n'
        return data

    @staticmethod
    def to_siesta_xyz_data(model):
        """Returns data for *.xyz file."""
        data = "  "
        nAtoms = model.n_atoms()
        data += str(nAtoms) + "\n"
        for i in range(0, nAtoms):
            data += "\n" + model.atoms[i].let + '       ' + model.xyz_string(i)
        return data

    @staticmethod
    def atoms_from_fdf_prepare(filename):
        number_of_atoms = TSIESTA.number_of_atoms(filename)
        atomic_coordinates_format = TSIESTA.atomic_coordinates_format(filename)
        lat = ""
        units = helpers.from_file_property(filename, 'ZM.UnitsLength', 1, 'string')
        if atomic_coordinates_format == "ScaledCartesian":
            lat = TSIESTA.lattice_constant(filename)
            units = "ang"
        if not units:
            if atomic_coordinates_format.lower().find("bohr") >= 0:
                units = "bohr"
            else:
                units = "ang"
        lat_vectors = TSIESTA.lattice_vectors(filename)
        if lat_vectors is None:
            lat_vectors = TSIESTA.lattice_parameters_abc_angles(filename)
        chem_spec_info = {}
        chemical_species_label = TSIESTA.get_block_from_siesta_fdf(filename, "ChemicalSpeciesLabel")
        for j in range(0, len(chemical_species_label)):
            row_data = chemical_species_label[j].split()
            chem_spec_info[row_data[0]] = [int(abs(int(row_data[1]))), row_data[2]]
        return atomic_coordinates_format, number_of_atoms, chem_spec_info, lat, lat_vectors, units

    @staticmethod
    def atoms_from_fdf_text(atomic_coordinates_format, number_of_atoms, chem_spec_info, lat, lat_vectors, lines, units):
        lines = clear_fdf_lines(lines)
        all_atoms = AtomicModel()
        at_list = []
        at_list1 = []
        i = 0
        is_block_atomic_coordinates = False
        is_block_z_matrix = False
        while i < len(lines):
            if lines[i].find("%block Zmatrix") >= 0:
                is_block_z_matrix = True
                i += 1
                at_list = []
                if lines[i].find("cartesian") >= 0:
                    for j in range(0, number_of_atoms):
                        i += 1
                        atom_full = lines[i].split()
                        at_list.append([float(atom_full[1]), float(atom_full[2]), float(atom_full[3]),
                                       (chem_spec_info[str(atom_full[0])])[1], (chem_spec_info[str(atom_full[0])])[0]])
            if lines[i].find("%block AtomicCoordinatesAndAtomicSpecies") >= 0:
                is_block_atomic_coordinates = True
                mult = 1
                if atomic_coordinates_format == "NotScaledCartesianBohr":
                    mult = 0.52917720859
                for j in range(0, number_of_atoms):
                    i += 1
                    atom_full = lines[i].split()
                    at_list1.append([mult * float(atom_full[0]), mult * float(atom_full[1]), mult * float(atom_full[2]),
                                    (chem_spec_info[str(atom_full[3])])[1], (chem_spec_info[str(atom_full[3])])[0]])
            i += 1
        if is_block_z_matrix:
            all_atoms = AtomicModel(at_list)
        else:
            if is_block_atomic_coordinates:
                all_atoms = AtomicModel(at_list1)
        if lat_vectors is None:
            all_atoms.set_lat_vectors_default()
        else:
            all_atoms.set_lat_vectors(lat_vectors[0], lat_vectors[1], lat_vectors[2])
        if is_block_z_matrix:
            if units.lower() == "bohr":
                all_atoms.convert_from_scaled_to_cart(0.52917720859)
        else:
            if is_block_atomic_coordinates:
                if atomic_coordinates_format == "ScaledByLatticeVectors":
                    all_atoms.convert_from_direct_to_cart()
                if atomic_coordinates_format == "ScaledCartesian":
                    all_atoms.convert_from_scaled_to_cart(lat)
        return all_atoms

    @staticmethod
    def atoms_from_ani(filename):
        """import from ANI file"""
        molecules = []
        if os.path.exists(filename):
            ani_file = open(filename)
            number_of_atoms = int(ani_file.readline())
            while number_of_atoms > 0:
                model = AtomicModel.atoms_from_xyz_structure(number_of_atoms, ani_file)
                molecules.append(model)
                st = ani_file.readline()
                if st != '':
                    number_of_atoms = int(st)
                else:
                    number_of_atoms = 0
        return molecules

    @staticmethod
    def atoms_from_output_cg(filename):
        """import from CG output"""
        period_table = TPeriodTable()
        molecules = []
        if os.path.exists(filename):
            number_of_atoms = TSIESTA.number_of_atoms(filename)
            sps = TSIESTA.get_species(filename)
            species_label_charges = ['null']
            for spec in sps:
                species_label_charges.append(spec[1])

            siesta_file = open(filename)
            sl = []
            isSpesF = 0
            need_to_convert1 = 0
            str1 = siesta_file.readline()
            atoms = []
            while str1 != '':
                if (str1 != '') and (str1.find("siesta: Atomic coordinates (Bohr) and species") >= 0) and (
                        isSpesF == 0):
                    str1 = siesta_file.readline()
                    while str1.find('siesta') >= 0:
                        str1 = helpers.spacedel(str1)
                        sl.append(int(str.split(str1, ' ')[4]))
                        str1 = siesta_file.readline()
                    isSpesF = 1

                if (str1 != '') and (str1.find("outcell: Unit cell vectors (Ang):") >= 0) and (isSpesF == 1):
                    lat_vect_1 = siesta_file.readline().split()
                    lat_vect_1 = helpers.list_str_to_float(lat_vect_1)
                    lat_vect_2 = siesta_file.readline().split()
                    lat_vect_2 = helpers.list_str_to_float(lat_vect_2)
                    lat_vect_3 = siesta_file.readline().split()
                    lat_vect_3 = helpers.list_str_to_float(lat_vect_3)

                    if len(atoms) > 0:
                        all_atoms = AtomicModel(atoms)
                        all_atoms.set_lat_vectors(lat_vect_1, lat_vect_2, lat_vect_3)
                        if need_to_convert1:
                            all_atoms.convert_from_direct_to_cart()
                            need_to_convert1 = 0
                        molecules.append(all_atoms)

                is_fractional_found = str1.find("outcoor: Atomic coordinates (fractional)") >= 0
                if is_fractional_found:
                    need_to_convert1 = 1

                is_angfound = str1.find("zmatrix: Z-matrix coordinates: (Ang ; rad )") >= 0
                is_bohr_found = str1.find("zmatrix: Z-matrix coordinates: (Bohr; rad )") >= 0
                mult = 1.0
                if is_bohr_found:
                    mult = 0.52917720859

                if (str1 != '') and (is_angfound or is_bohr_found or is_fractional_found) and (isSpesF == 1):
                    if not is_fractional_found:
                        for j in range(0, 2):
                            siesta_file.readline()
                    atoms = []

                    for i1 in range(0, number_of_atoms):
                        str1 = helpers.spacedel(siesta_file.readline())
                        s = str1.split(' ')
                        d1 = float(s[0]) * mult
                        d2 = float(s[1]) * mult
                        d3 = float(s[2]) * mult
                        charge = species_label_charges[sl[len(atoms)]]
                        c = period_table.get_let(charge)
                        atoms.append([d1, d2, d3, c, charge])
                str1 = siesta_file.readline()
            siesta_file.close()
        return molecules

    @staticmethod
    def atoms_from_output_md(filename):
        """import from MD output """
        periodTable = TPeriodTable()
        molecules = []
        if os.path.exists(filename):
            number_of_species = TSIESTA.number_of_species(filename)
            number_of_atoms = TSIESTA.number_of_atoms(filename)
            MdSiestaFile = open(filename)
            speciesLabel = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            sl = []
            isSpesFinde = 0
            isSpesF = 0
            str1 = MdSiestaFile.readline()
            while str1 != '':
                if (str1 != '') and (str1.find("siesta: Atomic coordinates (Bohr) and species") >= 0) and (
                        isSpesF == 0):
                    str1 = MdSiestaFile.readline()
                    while str1.find('siesta') >= 0:
                        str1 = helpers.spacedel(str1)
                        sl.append(int(str.split(str1, ' ')[4]))
                        str1 = MdSiestaFile.readline()
                    isSpesF = 1
                if (str1 != '') and (str1.find("ChemicalSpeciesLabel") >= 0) and (isSpesFinde == 0):
                    for i in range(0, number_of_species):
                        str1 = helpers.spacedel(MdSiestaFile.readline())
                        S = str.split(str1, ' ')
                        speciesLabel[int(S[0])] = S[1]
                    isSpesFinde = 1

                if (str1 != '') and (str1.find("Begin CG move") >= 0 or str1.find("Begin MD step") >= 0 or str1.find(
                        "Begin CG opt. move") >= 0):
                    if (str1 != '') and str1.find("Begin MD step") >= 0:
                        for j in range(0, 3):
                            MdSiestaFile.readline()
                    else:
                        if (str1.find("Begin CG move") >= 0) or (str1.find("Begin CG opt. move") >= 0):
                            while (str1 != '') and (str1.find("block") == -1) and (
                                    str1.find("outcoor: Atomic coordinates (Ang)") == -1):
                                str1 = MdSiestaFile.readline()

                    atoms = []
                    for i1 in range(0, number_of_atoms):
                        str1 = helpers.spacedel(MdSiestaFile.readline())
                        if str1 == "":
                            return []
                        S = str1.split(' ')
                        d1 = float(S[0])
                        d2 = float(S[1])
                        d3 = float(S[2])
                        Charge = speciesLabel[sl[len(atoms)]]
                        C = periodTable.get_let(Charge)
                        A = [d1, d2, d3, C, Charge]
                        atoms.append(A)
                    str1 = MdSiestaFile.readline()
                    while str1.find("outcell: Unit cell vectors (Ang):") == -1:
                        str1 = MdSiestaFile.readline()
                    vec1 = MdSiestaFile.readline().split()
                    vec1 = helpers.list_str_to_float(vec1)
                    vec2 = MdSiestaFile.readline().split()
                    vec2 = helpers.list_str_to_float(vec2)
                    vec3 = MdSiestaFile.readline().split()
                    vec3 = helpers.list_str_to_float(vec3)
                    AllAtoms = AtomicModel(atoms)
                    AllAtoms.set_lat_vectors(vec1, vec2, vec3)
                    molecules.append(AllAtoms)
                str1 = MdSiestaFile.readline()
            MdSiestaFile.close()
        return molecules

    @staticmethod
    def atoms_from_md_car(filename):
        """import from MD_CAR output """
        molecules = []
        if os.path.exists(filename):
            struct_file = open(filename)
            str1 = struct_file.readline()
            while str1.find("---") >= 0:
                newStr = AtomicModel()
                lat_const = float(struct_file.readline())
                lat1 = helpers.spacedel(struct_file.readline()).split()
                lat1 = helpers.list_str_to_float(lat1)
                lat1 = lat_const * np.array(lat1)
                lat2 = helpers.spacedel(struct_file.readline()).split()
                lat2 = helpers.list_str_to_float(lat2)
                lat2 = lat_const * np.array(lat2)
                lat3 = helpers.spacedel(struct_file.readline()).split()
                lat3 = helpers.list_str_to_float(lat3)
                lat3 = lat_const * np.array(lat3)
                numbers_of_atoms = helpers.spacedel(struct_file.readline()).split()
                numbers_of_atoms = helpers.list_str_to_int(numbers_of_atoms)
                str1 = struct_file.readline()
                if helpers.spacedel(str1) == "Direct":
                    for i in range(0, len(numbers_of_atoms)):
                        for j in range(0, numbers_of_atoms[i]):
                            row = helpers.spacedel(struct_file.readline()).split()
                            row = helpers.list_str_to_float(row)

                            let = "Direct"
                            charge = 200 + i
                            x = row[0]
                            y = row[1]
                            z = row[2]

                            newStr.add_atom(Atom([x, y, z, let, charge]))
                    newStr.set_lat_vectors(lat1, lat2, lat3)
                    newStr.convert_from_direct_to_cart()
                    molecules.append(newStr)
        return molecules

    @staticmethod
    def atoms_from_output_sp(filename):
        """Return the initial AtList from single point output file."""
        coord_format, n_atoms, chem_spec_info, lat, lat_vectors, units = TSIESTA.atoms_from_fdf_prepare(filename)
        line1 = "Dump of input data file"
        line2 = "End of input data file"
        lines = text_between_lines(filename, line1, line2)
        return [TSIESTA.atoms_from_fdf_text(coord_format, n_atoms, chem_spec_info, lat, lat_vectors, lines, units)]

    @staticmethod
    def atoms_from_output_optim(filename):
        """Return the relaxed AtList from output file."""
        number_of_atoms = TSIESTA.number_of_atoms(filename)
        species = TSIESTA.get_species(filename)
        at_list = []
        f1 = False
        f2 = False
        f3 = False
        n_vec = 0
        lat_vect_1 = ""
        lat_vect_2 = ""
        lat_vect_3 = ""
        mult = 1
        search1 = "outcoor: Relaxed atomic coordinates (Ang)"
        search2 = "outcoor: Relaxed atomic coordinates (Bohr)"
        search3 = "outcoor: Final (unrelaxed) atomic coordinates (Bohr)"

        for line in open(filename, 'r'):
            if line.find("outcell: Unit cell vectors (Ang):") > -1:
                f2 = True
                n_vec = 0
            else:
                if (n_vec == 0) and f2:
                    lat_vect_1 = line.split()
                    lat_vect_1 = helpers.list_str_to_float(lat_vect_1)
                if (n_vec == 1) and f2:
                    lat_vect_2 = line.split()
                    lat_vect_2 = helpers.list_str_to_float(lat_vect_2)
                if (n_vec == 2) and f2:
                    lat_vect_3 = line.split()
                    lat_vect_3 = helpers.list_str_to_float(lat_vect_3)
                    f2 = False
                if f2:
                    n_vec += 1

            if (line.find(search1) > -1) or (line.find(search2) > -1) or (line.find(search3) > -1):
                f1 = True
                if line.find("(Bohr)") > -1:
                    mult = 0.52917720859
            else:
                if (len(at_list) < number_of_atoms) and f1:
                    line1 = line.split()
                    line2 = [float(line1[0]) * mult, float(line1[1]) * mult, float(line1[2]) * mult, line1[5],
                             species[int(line1[3]) - 1][1]]
                    at_list.append(line2)
                if len(at_list) == number_of_atoms:
                    AllAtoms = AtomicModel(at_list)
                    AllAtoms.set_lat_vectors(lat_vect_1, lat_vect_2, lat_vect_3)
                    return [AllAtoms]
            if line.find("outcoor: Relaxed atomic coordinates (fractional)") > -1:
                f3 = True
            else:
                if (len(at_list) < number_of_atoms) and f3:
                    line1 = line.split()
                    line2 = [float(line1[0]), float(line1[1]), float(line1[2]), line1[5], species[int(line1[3]) - 1][1]]
                    at_list.append(line2)
                if len(at_list) == number_of_atoms:
                    AllAtoms = AtomicModel(at_list)
                    AllAtoms.set_lat_vectors(lat_vect_1, lat_vect_2, lat_vect_3)
                    AllAtoms.convert_from_direct_to_cart()
                    return [AllAtoms]
        return []

    @staticmethod
    def atoms_from_struct_out(filename):
        """import from STRUCT_OUT file"""
        period_table = TPeriodTable()
        molecules = []
        if os.path.exists(filename):
            struct_file = open(filename)
            lat1 = helpers.spacedel(struct_file.readline()).split()
            lat1 = helpers.list_str_to_float(lat1)
            lat2 = helpers.spacedel(struct_file.readline()).split()
            lat2 = helpers.list_str_to_float(lat2)
            lat3 = helpers.spacedel(struct_file.readline()).split()
            lat3 = helpers.list_str_to_float(lat3)
            number_of_atoms = int(struct_file.readline())

            new_str = AtomicModel()
            for i1 in range(0, number_of_atoms):
                str1 = helpers.spacedel(struct_file.readline())
                S = str1.split(' ')
                x = float(S[2])
                y = float(S[3])
                z = float(S[4])
                charge = int(S[1])
                let = period_table.get_let(charge)
                new_str.add_atom(Atom([x, y, z, let, charge]))
            new_str.set_lat_vectors(lat1, lat2, lat3)
            new_str.convert_from_direct_to_cart()
            molecules.append(new_str)
        return molecules

    @staticmethod
    def get_output_data(filename, fl, models, prop):
        type_of_run = (TSIESTA.type_of_run(filename).split())[0].lower()
        models = []
        if type_of_run != "sp":
            if fl != 'opt':
                models = TSIESTA.atoms_from_output_cg(filename)
                if len(models) == 0:
                    models = TSIESTA.atoms_from_output_md(filename)
            modelsopt = TSIESTA.atoms_from_output_optim(filename)
        else:
            modelsopt = TSIESTA.atoms_from_output_sp(filename)
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
