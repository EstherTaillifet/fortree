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
        self.callees = np.array("name", dtype='U200') # name

        # Init callees
        key = "call"
        target = self.path
        key_in = ["subroutine",self.name]
        key_out = ["end","subroutine", self.name]
        self.callees = pr.parse(key, target, key_in, key_out, output_file=False)


        # Init callers
        #key = ["call",self.name]
        #target = directory
        #self.callers = pr.parse(key, target, key_in=False, key_out=False, output_file=False)




