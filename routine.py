import sys
import os
import re
import numpy as np
import parser as pr


class Routine:

    def __init__(self, infos, directory):


        self.name = infos[0]
        self.path = infos[1]
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






