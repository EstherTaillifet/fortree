import sys
import os
import re
import numpy as np
import parser as pr


class TreeNode:

    def __init__(self, name, directory, keyword, root_path=False):
        self.name = name
        self.directory = directory
        self.root_path = root_path
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

    	# Find definition file of parent
        if (keyword == "program"):
            key = ["program", self.name]
        elif(keyword == "module"):
        	key = ["module", self.name]
        elif(keyword == "routine"):
        	key = ["subroutine", self.name]

        target = self.directory
        
        self.parent = pr.parse(key, target)
        if(np.size(self.parent) < 4):
            print("---------------------------------------------------------------")
            print("ERROR: ", keyword, " '", self.name, "' is not defined in one of the files contained in the given directory: ")
            print(self.directory)
            print("Please check the spelling.")
            print("---------------------------------------------------------------")
            sys.exit()

        if(np.size(self.parent) > 4):
            if(self.root_path):
            	del self.parent
            	self.parent = np.array(["name","path"], dtype='U200')
            	self.parent = np.vstack([self.parent,[self.name,self.root_path]])
            else:
                print("---------------------------------------------------------------")
                print("ERROR: ", keyword, " '", self.name, "' is defined in multiple files: ")
                for path in self.parent[1:,1]: 
                    print(path)
                print("Please give a specific ROOT_PATH in input.")
                print("---------------------------------------------------------------")
                sys.exit()               



    def init_used_modules(self, keyword):
        if(np.size(self.parent) < 4):
            self.init_parent(keyword)

        # Find used modules in parent definition file
        key = "use"
        target = self.parent[1,1]
        self.used_modules = pr.parse(key, target)

        # Find file definition for each module.
        n = np.shape(self.used_modules)
        nlines = n[0]
        for i in range(1,nlines-1): # Starts at 1 because the first line corrisponds to the coloumn tags.
            key = ["module",self.used_modules[i,0]] # self.used_modules[i,0] = module name
            target = self.directory
            tmp = pr.parse(key, target) # find module definition path.
            self.used_modules[i,1] = tmp[1,1] # renplace path by the definition path.


    def init_children(self, keyword):
        if(np.size(self.used_modules) < 4):
            self.init_used_modules(keyword)   

        # Find chilren and their definitiion files
        if(keyword == "routine"):
            key = "call"
            key_in = ["subroutine",self.name]
            key_out = ["end","subroutine", self.name]
            target = self.parent[1,1]
            self.children = pr.parse(key, target, key_in, key_out)
        else:
            key = "call"
            target = self.parent[1,1]
            self.children = pr.parse(key, target)
        self.clean_children()
        
        to_delete_indexes = np.array(-1,dtype=int)
        n = np.shape(self.children)
        nlines = n[0]
        for i in range(1,nlines-1): # Starts at 1 because the first line corrisponds to the coloumn tags.
            key = ["subroutine",self.children[i,0]] # self.children[i,0] = routine name
            target = self.directory
            tmp = pr.parse(key,target) # find routine definition path.
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





