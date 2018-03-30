import sys
import os
import re
import numpy as np
import parser as pr


class Routine:

    def __init__(self, infos, directory):


        self.name = infos[0]
        self.path = infos[1]
        #self.callers = np.array("name", dtype='U200') # name
        self.callees = np.array(["name"], dtype='U200') # name

        # Init callees
        key = "call"
        target = self.path
        key_in = ["subroutine",self.name]
        key_out = ["end","subroutine", self.name]
        tmp = pr.parse(key, target, key_in, key_out, output_file=False)
        
        if not isinstance(tmp, bool):
            self.callees = tmp
            self.callees = np.unique(self.callees, axis=0)

        # Init callers
        #key = ["call",self.name]
        #target = directory
        #self.callers = pr.parse(key, target, key_in=False, key_out=False, output_file=False)




