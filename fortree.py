import sys
import os
import re
import parser as pr
import render as rd
import program as prog
import module as mod
import routine as rout



class Fortree:

    def __init__(self):

        self.directory = ""
        self.program = ""
        self.module = ""
        self.routine = ""
        self.render_type = ""
        self.output_name = ""
        self.init_var()

    def init_var(self):
        if len(sys.argv) < 2:
            print("---------------------------------------------------------------")
            print("ERROR: An initalization file is needed.")
            print("USE: $ Python3 fortree.py init.txt")
            print("---------------------------------------------------------------")
            sys.exit()
        filename = sys.argv[1]
        self.directory = pr.get_init_value("DIRECTORY_TO_PARSE", filename)
        self.program = pr.get_init_value("RENDER_WHOLE_PROGRAM", filename)
        self.module = pr.get_init_value("RENDER_SINGLE_MODULE", filename)
        self.routine = pr.get_init_value("RENDER_SINGLE_ROUTINE", filename)
        self.render_type = pr.get_init_value("RENDER_TYPE", filename)
        self.output_name = pr.get_init_value("OUTPUT_NAME", filename)

    def print_var(self):
        print("---------------------------------------------------------------")
        print("directory = ",self.directory)
        print(
        "program = ", self.program, " | "
        "module = ", self.module, " | "
        "routine = ", self.routine
        )
        print(
        "render_type = ", self.render_type, " | "
        "output_name = ", self.output_name
        )
        print("---------------------------------------------------------------")



def main():
    print("===============================================================")
    print("=========================  FORTREE  ===========================")
    print("===============================================================")
    ft = ""
    p = ""
    m = ""
    r = ""

    ft = Fortree()
    ft.print_var()

    if(ft.program):
        p = prog.Program(ft)
        p.build_tree(ft)
    elif (ft.module):
        m = mod.Module(ft)
        m.build_tree(ft)
    elif (ft.routine):
        r = rout.Routine(ft)
        r.build_tree(ft)
    else:
        print("try to find a program")

    rd.render(ft)

if __name__ == "__main__":
    main()







