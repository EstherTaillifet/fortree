import sys
import os
import re
import numpy as np
import parser as pr


class TreeNode:

    def __init__(self, name, directory, keyword=None):
        self.name = name
        self.directory = directory
        self.parent = np.array(["name","path"], dtype='U200') # name, path
        self.children = np.array(["name","path"], dtype='U200') # name, path
        self.used_modules = np.array(["name","path"], dtype='U200') # name, path

        # Init parent
        self.init_parent(keyword)
        # Init used_modules
        self.init_used_modules(keyword)
        # Init children
        self.init_children(keyword)

    
    ''' 
    Initialization functions 
    '''
    def init_parent(self, keyword):
        if (keyword == "program"):
            match_key = ["program", self.name]
        elif(keyword == "module"):
        	match_key = ["module", self.name]
        elif(keyword == "routine"):
        	match_key = ["subroutine", self.name]

        # Find definition file of parent
        self.parent = pr.parse(match_key, self.directory)
        if(np.size(self.parent) < 4):
            print("---------------------------------------------------------------")
            print("ERROR: ", keyword, " '", self.name, "' is not defined in one of the files contained in the given directory: ")
            print(self.directory)
            print("Please check the spelling.")
            print("---------------------------------------------------------------")
            sys.exit()


    def init_used_modules(self, keyword):
        if(np.size(self.parent) < 4):
            self.init_parent(keyword)

        # Find used modules in parent definition file
        self.used_modules = pr.parse("use", self.parent[1,1])

        # Find file definition for each module.
        n = np.shape(self.used_modules)
        nlines = n[0]
        for i in range(1,nlines-1): # Starts at 1 because the first line corrisponds to the coloumn tags.
            key = ["module",self.used_modules[i,0]] # self.used_modules[i,0] = module name
            tmp = pr.parse(key, self.directory) # find module definition path.
            self.used_modules[i,1] = tmp[1,1] # renplace path by the definition path.


    def init_children(self, keyword):
        if(np.size(self.used_modules) < 4):
            self.init_used_modules(keyword)   

        # Find chilren and their definitiion files
        if(keyword == "routine"):
        	target = np.array(self.parent[1][1])
        	self.children = pr.parse("call", self.parent[1,1])
        else:
            self.children = pr.parse("call", self.parent[1,1])
        self.clean_children()
        
        to_delete_indexes = np.array(-1,dtype=int)
        n = np.shape(self.children)
        nlines = n[0]
        for i in range(1,nlines-1): # Starts at 1 because the first line corrisponds to the coloumn tags.
            key = ["subroutine",self.children[i,0]] # self.children[i,0] = routine name
            tmp = pr.parse(key, self.directory) # find routine definition path.
            if (np.size(tmp) < 4): # No match.
                to_delete_indexes = np.append(to_delete_indexes,i)
            elif(np.size(tmp) > 4): # Several matches.
                for tmppath in tmp[1:,1]: # Starts at 1 because the first line corrisponds to the coloumn tags.
                    for path in self.used_modules[1:,1]: # Starts at 1 because the first line corrisponds to the coloumn tags.
                        if(tmppath == path):
                            self.children[i,1] = path
                            break
            else: # Single match.
                Verif = False
                for path in self.used_modules[1:,1]: # Verify definition file is an included module definition file or parent file. Delete otherwise.
                    if(tmp[1,1] == path):
                        verif = True
                if (tmp[1,1] == self.parent[1,1]):
                    verif = True
                if verif:
                    self.children[i,1] = tmp[1,1]
                else:
                    to_delete_indexes = np.append(to_delete_indexes,i)

        if np.size(to_delete_indexes) > 1:
            to_delete_indexes = to_delete_indexes[1:]
            self.delete_child(to_delete_indexes)

    ''' 
    Visualization functions 
    '''
    def print_var(self):
        print("---------------------------------------------------------------")
        print(
        "Node name = ",self.name," | ", 
        "dimensions of parent array = ", np.shape(self.parent)," | ", 
        "dimensions of children array  = ", np.shape(self.children)," | ", 
        "dimensions of used_modules array = ",np.shape(self.used_modules)
        )
        print(" ")
        print("parent = ", self.parent)
        print(" ")
        print("children = ", self.children)
        print(" ")
        print("used_modules = ", self.used_modules)
        print("---------------------------------------------------------------")   	


    ''' 
    Operations on children
    '''
    def add_child(self, child):
        self.children = np.vstack([self.children, child])
        self.clean_children()
 

    def delete_child(self, irow):
    	if isinstance(irow, int):
    	    self.children = np.delete(self.children, irow, axis=0)
    	else:
            for i in irow:
                self.children = np.delete(self.children, irow, axis=0)



    def clean_children(self):
        tmp, indexes = np.unique(self.children,return_index=True, axis=0)
        indexes = np.sort(indexes)
        j=0
        for i in indexes:
        	tmp[j]=self.children[i]
        	j = j+1
        self.children = tmp





