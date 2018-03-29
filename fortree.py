import sys
import os
import numpy as np
import parser as pr
import render as rd
import treeNode as tn





class Fortree:

    def __init__(self):

        self.directory = ""
        self.root_path = ""
        self.program = ""
        self.module = ""
        self.routine = ""
        self.routines_list = ""
        self.modules_list = ""
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
        self.root_path = pr.get_init_value("ROOT_PATH", filename)
        self.program = pr.get_init_value("RENDER_WHOLE_PROGRAM", filename)
        self.module = pr.get_init_value("RENDER_SINGLE_MODULE", filename)
        self.routine = pr.get_init_value("RENDER_SINGLE_ROUTINE", filename)
        self.render_type = pr.get_init_value("RENDER_TYPE", filename)
        self.output_name = pr.get_init_value("OUTPUT_NAME", filename)

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

    def build_tree(self):

        # Start writing tree
        tree = rd.Render(self.output_name)
        tree.write_header()

        # Build root
        if self.program:
            root = tn.TreeNode(self.program, self.directory, keyword="program", root_path=self.root_path)
            #root.print_var()
        elif(self.module):
            root =  tn.TreeNode(self.module, self.directory, keyword="module", root_path=self.root_path)
            #root.print_var()
        elif(self.routine):
            root =  tn.TreeNode(self.routine, self.directory, keyword="routine", root_path=self.root_path)
            #root.print_var()
        else:
            tmp = pr.parse("program", self.directory)
            print(tmp)
            print("Try find program. Not implemented yet.")
            sys.exit()
  
        # Build levels
        self.build_node(root, tree)

        # End writing tree
        tree.write_footer()
        tree.render()

    def build_node(self, parent_node_obj, tree):
        print("------------------------- New node ----------------------------")
        print("New parent = ", parent_node_obj.name)
        #print("Children to consider = ", parent_node_obj.children[1:])
        for child in parent_node_obj.children[1:]:
            tree.write(parent_node_obj.name, child[0])
            #print("Current child: ", child[0])
            #print("Current child path: ", child[1])
            node =  tn.TreeNode(child[0], self.directory, keyword="routine", root_path=child[1])
            if np.size(node.children) > 2:
                #print("Current child's children = ",node.children[1:])
                self.build_node(node, tree)


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
    elif(ft.render_type == "CALL_GRAPH"):
        print("call graph") # ft.build_graph()

    #ft.render_tree()

if __name__ == "__main__":
    main()







