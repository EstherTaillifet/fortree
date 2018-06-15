import sys
import os
import numpy as np
import parser as pr
import render as rd
import treeNode as tn
import routine as rt
import time




class Fortree:

    def __init__(self):

        # Init file var
        self.directory = ""
        self.root_path = ""
        self.program = ""
        self.module = ""
        self.routine = ""
        self.render_type = ""
        self.show_only_def =""
        self.output_name = ""

           
        # Init tree var
        self.root = ""
        self.routines_list = ""
        self.tree_arr = ""

        self.init_file_var()
        self.init_tree_var()
        
    def print_var(self):
        print("---------------------------------------------------------------")
        print("directory = ",self.directory)
        print("root path = ",self.root_path)
        print(
        "program to render = ", self.program, " | "
        "module to render = ", self.module, " | "
        "routine to render = ", self.routine
        )
        print(
        "render type = ", self.render_type, " | "
        "show only def = ", self.show_only_def, " | "
        "output name = ", self.output_name
        )
        print("---------------------------------------------------------------")

    def init_file_var(self):

        if len(sys.argv) < 2:
            print("---------------------------------------------------------------")
            print("ERROR: An initalization file is needed.")
            print("USE: $ Python3 fortree.py init.txt")
            print("---------------------------------------------------------------")
            sys.exit()

        filename = sys.argv[1]

        self.directory = pr.get_init_value("DIRECTORY_TO_PARSE", filename)
        self.root_path = pr.get_init_value("ROOT_PATH", filename)
        self.program = pr.get_init_value("RENDER_WHOLE_PROGRAM", filename)
        self.module = pr.get_init_value("RENDER_SINGLE_MODULE", filename)
        self.routine = pr.get_init_value("RENDER_SINGLE_ROUTINE", filename)
        self.render_type = pr.get_init_value("RENDER_TYPE", filename)
        self.show_only_def = pr.get_init_value("SHOW_ONLY_DEF", filename)
        self.output_name = pr.get_init_value("OUTPUT_NAME", filename)

        


    def init_tree_var(self):

        if(len(self.directory) < 1):
            self.init_file_var()

        # Build routines list

        pre_list = pr.parse("subroutine", self.directory) # routine name , definition file path

        # List of objects that are instances of Routine class.
        self.routines_list = [ rt.Routine(one_routine[0], one_routine[1], pre_list) for one_routine in pre_list[1:]]


        # Build root
        if self.program:
            self.root = tn.TreeNode(self.program, self.directory, self.routines_list, keyword="program", root_path=self.root_path)
        elif(self.module):
            self.root =  tn.TreeNode(self.module, self.directory, self.routines_list, keyword="module", root_path=self.root_path)
        elif(self.routine):
            self.root =  tn.TreeNode(self.routine, self.directory, self.routines_list, keyword="routine", root_path=self.root_path)
        else:
            tmp = pr.parse("program", self.directory)
            print(tmp)
            print("Try find program. Not implemented yet.")
            sys.exit()
        if(self.render_type == "CALL_TREE"):
            self.tree_arr = np.array(["caller", "callee", "callee_path"], dtype='U200')
        else:
            self.tree_arr = np.array(["parent", "child"], dtype='U200')



    def build_tree(self):

        # Build root
        if not isinstance(self.root, tn.TreeNode):
            self.init_tree_var()
  
        # Build levels
        level = 0
        self.build_node(self.root, level)

        return self.tree_arr


    def build_node(self, parent_node_obj, level=False):

        if isinstance(level,int):
            level = level+1

        if (np.size(parent_node_obj.children) > 2):
            for child in parent_node_obj.children[1:]:
                self.tree_arr=np.vstack([self.tree_arr, [parent_node_obj.name, child[0], child[1]]])
                node =  tn.TreeNode(child[0], self.directory, self.routines_list, keyword="routine", root_path=child[1])
                self.build_node(node, level)
        
        return True

    def build_graph(self):
        print("Call graph is not implemented yet.")
        sys.exit()


def main():
    print("===============================================================")
    print("=========================  FORTREE  ===========================")
    print("===============================================================")
    ft = ""


    ft = Fortree()
    ft.print_var()

    if(ft.render_type == "CALL_TREE"):
        ft.build_tree()

        #clean duplicates
        ft.tree_arr = np.unique(ft.tree_arr, axis=0)

        # write tree
        ftree = rd.Render(ft.output_name)

        ftree.write_header()

        if ft.show_only_def:
            for element in ft.tree_arr:
                if element[2] != "ND": 
                    ftree.write(element[0], element[1])
        else:
            for element in ft.tree_arr:
                ftree.write(element[0], element[1])
        ftree.write_footer()
        ftree.render()

    elif(ft.render_type == "CALL_GRAPH"):
        ft.build_graph()



if __name__ == "__main__":

    start_time = time.time()
    main()
    print("===============================================================")
    print("Fortree took %s seconds to run." % (time.time() - start_time))
    print("===============================================================")
    







