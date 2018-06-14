import sys
import os
import re
import numpy as np
import parser as pr


class Routine:

    def __init__(self, name, path, pre_list):

        self.name = name
        self.path = path
        self.callees = np.array(["name", "path"], dtype='U200') # name
        self.used_modules = np.array(["name", "path"], dtype='U200') # name

        # Init used_modules
        self.init_used_modules()

        # Init callees
        self.init_callees(pre_list)


    def init_used_modules(self):

        key = "use"
        target = self.path
        tmp = pr.parse(key, target)
        
        if not isinstance(tmp, bool):
            self.used_modules = tmp
            self.used_modules = np.unique(self.used_modules, axis=0) 


    def init_callees(self, pre_list):

        if(np.size(self.used_modules) < 4):
            self.init_used_modules()

        key = "call"
        target = self.path
        key_in = ["subroutine",self.name]
        key_out = ["end","subroutine", self.name]
        tmp = pr.parse(key, target, key_in, key_out, output_file=True)
        
        if not isinstance(tmp, bool):
            self.callees = tmp
            callees_tmp = self.callees[1:]
            callees_tmp = np.unique(callees_tmp, axis=0)
            self.callees = np.array(["name", "path"], dtype='U200')
            for callee in callees_tmp:
                self.callees = np.vstack([self.callees, [callee]])

        # Definition path for callees
        i=1
        if np.size(self.callees) > 2:
            for callee in self.callees[1:]:
                self.callees[i,1] = "ND" # ND = "Non Defined" in current code (may be a routine part of the fortran language)
                for routine in pre_list[1:]:
                    if routine[0] == callee[0]:
                        self.callees[i,1]=routine[1]
                i=i+1



            






