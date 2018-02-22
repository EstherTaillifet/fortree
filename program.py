import sys
import os
import re
import parser as pr
import render as rd
import numpy as np


class Program:

    """
    Initialization functions
    """
    def __init__(self, fortree_obj):
        # Program variables declaration
        self.program_infos = np.array(["program_name","def_filename","def_filepath"])
        self.used_module_list = np.array(["module_name","def_filename","def_filepath"])
        self.defined_routine_list = np.array(["routine_name","def_filename","def_filepath"])

        # Variables initialisation
        self.init_program_infos(fortree_obj)
        self.init_module_list(fortree_obj)
        self.init_routine_list(fortree_obj)

        # Initialised variables display
        self.print_var()

    def init_program_infos(self, fortree_obj):
        key = ["program",fortree_obj.program]
        temp_path = pr.find_path(key,fortree_obj.directory)
        self.program_infos = [fortree_obj.program, pr.get_filename_from_path(temp_path), temp_path]
        del temp_path
        return self.program_infos

    def init_module_list(self, fortree_obj):
        if self.program_infos[0] == "program_name":
            self.init_program_infos(fortree_obj)

        temp_path = ""
        key = ""
        temp_module_list = self.used_module_list
        used_module_names = pr.get_match("use", self.program_infos[2]) # finds the names of modules used in the main program file.

        for module in used_module_names: # for each used modules
            key = ["module", module]
            temp_path = pr.find_path(key, fortree_obj.directory) # finds the path of the file in which it is defined.
            if len(temp_path) > 1:
                to_append = [module, pr.get_filename_from_path(temp_path), temp_path]
                temp_module_list = np.append(temp_module_list, to_append)
        
        self.used_module_list = temp_module_list[3:]

        return self.used_module_list

    def init_routine_list(self, fortree_obj):
        if self.program_infos[0] == "program_name":
            self.init_program_infos(fortree_obj)

        temp_routine_list = self.defined_routine_list
        defined_subroutine_names = pr.get_match("subroutine", self.program_infos[2]) # finds the names of subroutines 
        defined_function_names = pr.get_match("function", self.program_infos[2]) # and functions defined in the main program file.

        defined_routine_names = np.hstack( (defined_subroutine_names, defined_function_names) )

        for routine in defined_routine_names:
            to_append = [routine, self.program_infos[1], self.program_infos[2]]
            temp_routine_list = np.append(temp_routine_list, to_append)

        self.defined_routine_list = temp_routine_list[3:]
        return self.defined_routine_list


    """
    Other stuff
    """

    def print_var(self):
        print("---------------------------------------------------------------")
        print("program_infos = ",self.program_infos)
        print("used_module_list = ", self.used_module_list)
        print("defined_routine_list = ", self.defined_routine_list)
        print("---------------------------------------------------------------")

    def build_tree(self, fortree_obj):
        if(fortree_obj.render_type == "CALL_TREE" or fortree_obj.render_type == "CALL_GRAPH"):
            pass

        print("build tree")
















