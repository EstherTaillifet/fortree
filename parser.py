import os
import re
import numpy as np



"""
Functions related to parsing initialization file
"""

def get_init_value(key,filename):
    file = open(filename, "r")
    re_to_match = "^"+key+"\s+(\S+)"
    match = re.findall(re_to_match, file.read(),re.MULTILINE)
    file.close()
    val = check_init_value(key, match[0])
    return val


def check_init_value(key, val):

    val_out = False
    ok_val = []

    if (key == "DIRECTORY_TO_PARSE"):
        match = re.findall("\/[^,:]*", val)
        if match:
        	val_out = val
        else:
            val_out = os.getcwd()

        if val_out[len(val_out)-1] == "/":
            val_out = val_out[0:len(val_out)-1]

    elif (key == "RENDER_WHOLE_PROGRAM"):
        if val != "NONE":
            val_out = val
    elif (key == "RENDER_SINGLE_MODULE"):
        if val != "NONE":
            val_out = val
    elif(key == "RENDER_SINGLE_ROUTINE"):
        if val != "NONE":
            val_out = val
    elif(key == "RENDER_TYPE"):
        ok_val = ["CALL_TREE","CALL_GRAPH","DEF_TREE"]
        if val in ok_val:
            val_out = val  
    elif(key == "OUTPUT_NAME"):
        match = re.findall("\w+", val)
        if not match:
            val_out = "fotree"
        else:
            val_out = val

    return val_out


"""
Functions related to parsing fortran program files
"""

def parse(fortree_obj):

    print("parse")



def get_match(key, path):
    """
    Returns an array of words given after the key_to_match in the file accessed by path.
    key_to_match can be a couple of words.
    """ 

    # local variables
    outpout = []
    match = None
    matches = None
    file_name = None
    re_to_search = ""


    if is_fortran_extension_file(path):
        # extract word after keyword or key_to_match group from file
        if len(key[0]) > 1 and len(key[1]) > 1:
            for k in key:
                re_to_search = re_to_search+"\s+"+k
            re_to_search = re_to_search[3:]+"\s"
        else:
            re_to_search = "^(?!!)(\s*"+key+"\s+(\w+))"
        file = open(path,"r")
        matches = re.findall(re_to_search, file.read(), re.IGNORECASE | re.MULTILINE)
        file.close()

        # Prepare output
        for match in matches:
            outpout.append(match[1])
    
    # delete local variables
    del match
    del matches
    del file_name
    del re_to_search

    return outpout


def find_path(key, directory):
    """
    Returns a string or several strings of the path or paths of the files that contains the word or words contained in key.
    The key can be a string or an array of two strings word 1 and word 2. 
    In this case, it will matches the built expression word 1 followed by word 2.
    """ 
    file_path = ""
    temp_output = np.chararray([1,2])


    if not os.path.isdir(directory):
        print("---------------------------------------------------------------")
        print("ERROR: ", directory, "is not a directory or doesn't exist.")
        print("---------------------------------------------------------------")
        sys.exit()
    for path, subdir_list, file_list in os.walk(directory):

        for file in file_list:
            file_path = path + "/" + file

            if np.size(key) == 1:
                key_to_match = key
                file_match = get_match(key_to_match,file_path)
                if file_match:
                    temp_output = np.append(temp_output, [file_match[0], file_path])

            elif np.size(key) == 2:
                key_to_match = [key[0],key[1]]
                file_match = get_match(key_to_match,file_path)
                if file_match:
                    output = file_path


    if not 'output' in locals():
        output = temp_output[2:]
        del temp_output

    return output


def is_fortran_extension_file(path):
    match = re.search("(\w+.f90)", path, re.IGNORECASE)
    if match:
        return match[0]
    else:
        return False

def get_filename_from_path(path):
    match = re.search("\w+\.(.+)$", path, re.IGNORECASE)
    if match:
        return match[0]
    else:
        return False

