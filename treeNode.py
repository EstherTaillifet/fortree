import sys
import os
import re
import numpy as np
import parser as pr
import time


class TreeNode:

    def __init__(self, name, directory, routines_list, keyword, root_path=False):
        self.name = name
        self.directory = directory
        self.root_path = root_path
        self.parent = np.array(["name","path"], dtype='U200') # name, path
        self.children = np.array(["name","path"], dtype='U200') # name, path

        # Init parent
        self.init_parent(keyword, routines_list)

        # Init children     
        self.init_children(keyword, routines_list)
    
    ''' 
    Initialization functions 
    '''
    def init_parent(self, keyword, routines_list):

        if self.root_path:
            self.parent = np.vstack([self.parent,[self.name,self.root_path]])
        else: 

            if (keyword == "program"):
                key = ["program", self.name]
            elif(keyword == "module"):
                key = ["module", self.name]
 
            target = self.directory
           
            tmp = pr.parse(key, target)
            if not (isinstance(tmp, bool)):
                self.parent = tmp
    
            if(np.size(self.parent) < 4):
                print("---------------------------------------------------------------")
                print("ERROR: ", keyword, " '", self.name, "' is not defined in one of the files contained in the given directory: ")
                print(self.directory)
                print("---------------------------------------------------------------")
                sys.exit()
    
            if(np.size(self.parent) > 4):
                print("---------------------------------------------------------------")
                print("ERROR: ", keyword, " '", self.name, "' is defined in multiple files: ")
                for path in self.parent[1:,1]: 
                    print(path)
                print("Please specify a ROOT_PATH in the input file.")
                print("---------------------------------------------------------------")
                sys.exit() 



    def init_children(self, keyword, routines_list):

        # Find chilren and their definitiion files
        if(keyword == "routine"):

            for routine in routines_list[1:]:
                if routine.name == self.name and routine.name != "name":
                    if np.size(routine.callees) > 1:
                        self.children = routine.callees[1:]
                    return
            #print(self.children)

        else:

            if(keyword == "program"):
                key = "call"
                target = self.parent[1,1]
                key_in = ["program",self.parent[1,0]]
                key_out = ["end","program", self.parent[1,0]]
                tmp = pr.parse(key, target, key_in, key_out, output_file=True)
            elif(keyword == "module"):
                key = "call"
                target = self.parent[1,1]
                key_in = ["module",self.parent[1,0]]
                key_out = ["end","module", self.parent[1,0]]
                tmp = pr.parse(key, target, key_in, key_out, output_file=True)                
            
            if not isinstance(tmp, bool):
                self.children = tmp
                self.children = self.clean(self.children)
            n = int(np.size(self.children)/2)

            children = self.children

            i=1
            for child in children[1:]:
                self.children[i,1] = "ND"
                for routine in routines_list:
                    if routine.name == child[0]:
                        self.children[i,1] = routine.path
                i=i+1


            

    ''' 
    Visualization functions 
    '''
    def print_var(self):
        print("---------------------------------------------------------------")
        print(
        "Node name = ",self.name," | ", 
        "dimensions of parent array = ", np.shape(self.parent)," | ", 
        "dimensions of children array  = ", np.shape(self.children)," | ", 
        )
        print(" ")
        print("parent = ", self.parent)
        print(" ")
        print("children = ", self.children)
        print(" ")
        print("---------------------------------------------------------------")   	


    ''' 
    Operations on treeNodes elements.
    '''

    def delete(self, arr, irow):
        if isinstance(irow, int):
            if (irow > -1):
                arr = np.delete(arr, irow, axis=0)
        else:
            if np.size(irow) > 1:
                for i in irow:
                    arr = np.delete(arr, irow, axis=0)
        return arr


    def clean(self, arr):
        tmp, indexes = np.unique(arr,return_index=True, axis=0)
        indexes = np.sort(indexes)
        j=0
        for i in indexes:
            tmp[j]=arr[i]
            j = j+1
        arr = tmp
        return arr





