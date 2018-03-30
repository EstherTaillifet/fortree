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
        self.output_name = ""
           
        # Init tree var
        self.root = ""
        self.routines_list = ""
        self.modules_list = ""

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
        self.output_name = pr.get_init_value("OUTPUT_NAME", filename)

        


    def init_tree_var(self):

        if(len(self.directory) < 1):
            self.init_file_var()


        # Build routines list
        tmp_list = pr.parse("subroutine", self.directory) # routine name , definition file path

        # List of objects that are instances of Routine class.
        self.routines_list = [ rt.Routine(one_routine, self.directory) for one_routine in tmp_list[1:]]

        # Build root
        if self.program:
            self.root = tn.TreeNode(self.program, self.directory, self.routines_list, keyword="program", root_path=self.root_path)
            #root.print_var()
        elif(self.module):
            self.root =  tn.TreeNode(self.module, self.directory, self.routines_list, keyword="module", root_path=self.root_path)
            #root.print_var()
        elif(self.routine):
            self.root =  tn.TreeNode(self.routine, self.directory, self.routines_list, keyword="routine", root_path=self.root_path)
            #root.print_var()
        else:
            tmp = pr.parse("program", self.directory)
            print(tmp)
            print("Try find program. Not implemented yet.")
            sys.exit()




        #n = np.shape(tmp_list)
        
        #for i in range(0, n[0]-1):
        #    print('-------------------------------------------------')
        #    print(self.routines_list[i].name)
        #    print(self.routines_list[i].path)
        #    print(self.routines_list[i].callees)


    def build_tree(self):

        # Start writing tree
        ftree = rd.Render(self.output_name)
        ftree.write_header()

        # Build root
        if not isinstance(self.root, tn.TreeNode):
            self.init_tree_var()
  
        # Build levels
        self.build_node(self.root, ftree)

        # End writing tree
        ftree.write_footer()
        ftree.render()

    def build_node(self, parent_node_obj, ftree):
        print("------------------------- New node ----------------------------")
        print("New parent = ", parent_node_obj.name)
        print("Children to consider = ", parent_node_obj.children[1:])
        for child in parent_node_obj.children[1:]:
            ftree.write(parent_node_obj.name, child[0])
            #print("Current child: ", child[0])
            #print("Current child path: ", child[1])
            node =  tn.TreeNode(child[0], self.directory, self.routines_list, keyword="routine", root_path=child[1])
            if np.size(node.children) > 2:
                #print("Current child's children = ",node.children[1:])
                self.build_node(node, ftree)


        return True


    #def render_tree(self):
    #    rd.render(self)
    #    return True



def main():
    print("===============================================================")
    print("=========================  FORTREE  ===========================")
    print("===============================================================")
    ft = ""


    ft = Fortree()
    ft.print_var()

    if(ft.render_type == "CALL_TREE"):
        ft.build_tree()
        print("call tree")
    elif(ft.render_type == "CALL_GRAPH"):
        print("call graph") # ft.build_graph()

    #ft.render_tree()

if __name__ == "__main__":

    start_time = time.time()
    main()
    print("===============================================================")
    print("Fortree took %s seconds to run." % (time.time() - start_time))
    print("===============================================================")
    







