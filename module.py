import sys
import os
import re
import numpy as np
import parser as pr


class Module:

    def __init__(self, name, path, pre_list):

        self.name = name
        self.path = path
        self.def_routines = np.array(["name","path"], dtype='U200') # Routines called by self.name. 
        self.uses = np.array(["name", "path"], dtype='U200') # Routines called by self.name.  path = definition file path.


        # Init defined routines
        self.init_def_routines()

        # Init used modules
        self.init_uses(pre_list)


    def init_def_routines(self):

        key = "subroutine"
        target = self.path
        key_in = ["module",self.name]
        key_out = ["end","module", self.name]
        tmp = pr.parse(key, target, key_in, key_out, output_file=True)

        # Clean duplicates
        if not isinstance(tmp, bool):
            self.def_routines = tmp
            def_routines_tmp = self.def_routines[1:]
            def_routines_tmp = np.unique(def_routines_tmp, axis=0)
            self.def_routines = np.array(["name","path"], dtype='U200')
            for routine in def_routines_tmp:
                self.def_routines = np.vstack([self.def_routines, [routine[0], routine[1]]])
        

    def init_uses(self, pre_list):

        key = "use"
        target = self.path
        tmp = pr.parse(key, target, output_file=True)

        # Clean duplicates
        if not isinstance(tmp, bool):
            self.uses = tmp
            uses_tmp = self.uses[1:]
            uses_tmp = np.unique(uses_tmp, axis=0)
            self.uses = np.array(["name","path"], dtype='U200')
            for use in uses_tmp:
                self.uses = np.vstack([self.uses, [use]])

        # Definition path for callees
        i=1
        if np.size(self.uses) > 2:
            for use in self.uses[1:]:
                self.uses[i,1] = "ND" # ND = "Non Defined" in current code (may be a routine part of the fortran language)
                for module in pre_list[1:]:
                    if module[0] == use[0]:
                        self.uses[i,1]=module[1]
                i=i+1



            






