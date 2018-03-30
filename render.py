import os
import numpy as np


class Render:
    def __init__(self, name):
    	self.name = name
    	self.gv_file = open(name+".gv","w")

    def write_header(self):
        self.gv_file.write("digraph G {")
        self.gv_file.write("\n "+'rankdir="LR"')

    def write_footer(self):
        self.gv_file.write("\n }")
        self.gv_file.close()

    def write(self, word1,word2):
        self.gv_file.write("\n "+word1+"->"+word2)

    def render(self):
        os.system("dot -Teps -o "+self.name+".eps "+self.name+".gv")
        print("---------------------------------------------------------------")
        print("Render done.")
        print("---------------------------------------------------------------")
