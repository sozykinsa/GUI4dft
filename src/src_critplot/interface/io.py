# -*- coding: utf-8 -*-

import os
from copy import deepcopy
from core_atomistic import helpers
from src_critplot.programs.topond import TopondModelCP
from src_critplot.programs.critic2 import Critic2ModelCP
from src_critplot.interface.cp_project_file import CritPlotProjectFile
from src_critplot.models.cp_model import AtomicModelCP


class ImporterExporter(object):

    @staticmethod
    def import_from_file(filename: str, is_add_translations = False):
        """import file"""
        model: AtomicModelCP = None
        is_critic_open = False
        if os.path.exists(filename):
            file_format = helpers.check_format(filename)
            print("format: ", file_format)
            if file_format == "topond_out":
                model = TopondModelCP(filename, is_add_translations)
            elif file_format == "critic_cro":
                model = Critic2ModelCP(filename)
                is_critic_open = True
            elif file_format == "project":
                model = CritPlotProjectFile.project_file_reader(filename)
            else:
                print("Wrong format")
        return [model], is_critic_open

    @staticmethod
    def model_for_export(model: AtomicModelCP):
        new_model = deepcopy(model)
        new_model.translated_atoms_remove()
        return new_model

    @staticmethod
    def export_to_file(model, file_name):  # pragma: no cover
        new_model = ImporterExporter.model_for_export(model)
        if file_name.endswith(".data"):
            text = CritPlotProjectFile.project_file_writer(new_model)
            helpers.write_text_to_file(file_name, text)
