import sys
import os
import numpy as np
import parser as pr
import render as rd
import treeNode as tn
import routine as rt
import module as md
import time




class Fortree:

    def __init__(self):

        # Init file var
        self.directory = ""
        self.root_path = ""
        self.program = ""
        self.module = ""
        self.routine = ""
        self.fortree_type = ""
        self.branch_type = ""
        self.show_only_def =""
        self.output_name = ""
        self.n_levels = ""
        self.tree_root_name = ""
        self.tree_root_type = ""
  
        # Init tree var
        self.root = ""
        self.routines_list = ""
        self.modules_list = ""
        self.tree_arr = ""

        self.init_file_var()
        self.init_tree_var()
        
    def print_var(self):
        print("---------------------------------------------------------------")
        print("Directory = ",self.directory)
        print("Root path = ",self.root_path)
        print("Tree root type = ", self.tree_root_type)
        print("Tree root name = ", self.tree_root_name)
        print("Render type = ", self.fortree_type)
        print("Show only def = ", self.show_only_def)
        print("N levels to render = ", self.n_levels)
        print("Output name = ", self.output_name)
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
        self.root_path = pr.get_init_value("ROOT_FILE_PATH", filename)
        self.tree_root_name = pr.get_init_value("TREE_ROOT_NAME", filename)
        self.tree_root_type = pr.get_init_value("TREE_ROOT_TYPE", filename)
        if (self.tree_root_type == "PROGRAM"):
            self.program = self.tree_root_name
        elif(self.tree_root_type == "MODULE"):
            self.module = self.tree_root_name
        elif(self.tree_root_type == "ROUTINE"):
            self.routine = self.tree_root_name
        self.n_levels = pr.get_init_value("N_LEVELS", filename)
        self.fortree_type = pr.get_init_value("FORTREE_TYPE", filename)
        self.show_only_def = pr.get_init_value("SHOW_ONLY_DEF", filename)
        self.output_name = pr.get_init_value("OUTPUT_NAME", filename)

        


    def init_tree_var(self):

        if(len(self.directory) < 1):
            self.init_file_var()

        # Build routines list
        pre_rout_list = pr.parse("subroutine", self.directory) # routine name , definition file path

        # List of objects that are instances of Routine class.
        self.routines_list = [ rt.Routine(one_routine[0], one_routine[1], pre_rout_list) for one_routine in pre_rout_list[1:]]

        # Build modules list
        pre_mod_list = pr.parse("module", self.directory) # modules name , definition file path
        pre_mod_list_tmp = pre_mod_list[1:]
        pre_mod_list_tmp = np.unique(pre_mod_list_tmp, axis=0)
        pre_mod_list = np.array(["name", "path"], dtype='U200')
        for pre_mod_tmp in pre_mod_list_tmp:
            pre_mod_list = np.vstack([pre_mod_list, [pre_mod_tmp]])


        # List of objects that are instances of Module class.
        self.modules_list = [ md.Module(one_module[0], one_module[1], pre_mod_list) for one_module in pre_mod_list[1:]]


        # Build root

        if(self.fortree_type == "DEF_TREE" or self.fortree_type == "DEP_TREE"):
            self.branch_type = "DEF"
        elif (self.fortree_type == "CALL_TREE"):
            self.branch_type = "CALL"

        if self.program:
            self.root = tn.TreeNode(self.program, self.directory, self.routines_list, self.modules_list, self.branch_type, keyword="program", root_path=self.root_path)
        elif(self.module):
            self.root =  tn.TreeNode(self.module, self.directory, self.routines_list, self.modules_list, self.branch_type, keyword="module", root_path=self.root_path)
        elif(self.routine):
            self.root =  tn.TreeNode(self.routine, self.directory, self.routines_list, self.modules_list, self.branch_type, keyword="routine", root_path=self.root_path)
        else:
            tmp = pr.parse("program", self.directory)
            print(tmp)
            print("Try find program. Not implemented yet.")
            sys.exit()
        
        # Out-put tree array
        if(self.fortree_type == "CALL_TREE"):
            self.tree_arr = np.array(["caller", "callee", "callee_path"], dtype='U200')
        elif(self.fortree_type == "DEF_TREE"):
            self.tree_arr = np.array(["parent", "defined","path"], dtype='U200')
        elif(self.fortree_type == "DEP_TREE"):
            self.tree_arr = np.array(["module", "user","path"], dtype='U200')
        else:
            self.tree_arr = np.array(["parent", "child", "path"], dtype='U200')



    def build_tree(self):

        # Build root
        if not isinstance(self.root, tn.TreeNode):
            self.init_tree_var()
  
        # Build levels
        if(self.fortree_type == "CALL_TREE"):
            level = 0
            self.branch_type = "CALL"
            self.build_node(self.root, level)

        elif(self.fortree_type == "DEP_TREE"):
            if (np.size(self.root.children) > 1):
                for child in self.root.children[1:]:
                    for module in self.modules_list:
                        if (np.size(module.uses) > 2):
                            for use in module.uses:
                                if use[1] == child[1]:
                                    self.tree_arr=np.vstack([self.tree_arr, [self.root.name, module.name, module.path]])

        elif(self.fortree_type == "DEF_TREE"):
            self.branch_type = "DEF"
            if (np.size(self.root.children) > 1):
                for child in self.root.children[1:]:
                    self.tree_arr=np.vstack([self.tree_arr, [self.root.name, child[0], child[1]]])

        return self.tree_arr


    def build_node(self, parent_node_obj, level=False):

        if isinstance(level,int):
            level = level+1
            if level == self.n_levels:
                return

        if (np.size(parent_node_obj.children) > 2):
            for child in parent_node_obj.children[1:]:
                self.tree_arr=np.vstack([self.tree_arr, [parent_node_obj.name, child[0], child[1]]])
                node =  tn.TreeNode(child[0], self.directory, self.routines_list, self.modules_list, self.branch_type, keyword="routine", root_path=child[1])
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


    if(ft.fortree_type == "CALL_TREE" or ft.fortree_type == "DEF_TREE" or ft.fortree_type == "DEP_TREE"):
        ft.build_tree()

        #clean duplicates
        ft.tree_arr = np.unique(ft.tree_arr, axis=0)

        if(np.size(ft.tree_arr) > 2):
            # write tree
            ftree = rd.Render(ft.output_name)
    
            ftree.write_header()

            if ft.show_only_def:
                for element in ft.tree_arr:
                    if(ft.fortree_type == "CALL_TREE" and element[2] != "ND"): 
                        ftree.write(element[0], element[1])
                    else:
                        ftree.write(element[0], element[1])
            else:
                for element in ft.tree_arr:
                    ftree.write(element[0], element[1])
            ftree.write_footer()
            ftree.render()
        else:
            print("No child.")

    elif(ft.fortree_type == "CALL_GRAPH"):
        ft.build_graph()



if __name__ == "__main__":

    start_time = time.time()
    main()
    print("===============================================================")
    print("Fortree took %s seconds to run." % (time.time() - start_time))
    print("===============================================================")
    







