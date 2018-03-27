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

    elif (key == "ROOT_PATH"):
        match = re.findall("\/[^,:]*", val)
        if match:
            val_out = val

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
            val_out = "fortree"
        else:
            val_out = val

    return val_out


"""
Functions related to parsing fortran program files
"""


def get_match(key, path):
    """
    Returns an array of words given after the key in the file accessed by path.
    key can be a couple of words.
    """ 

    # local variables
    outpout = []
    match = ""
    matches = ""
    file_name = ""
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
    




def parse(key, target , boundary_in=False, boundary_out=False, output_file=True):
    """
    key: word or couple of words to match.
    target: path or directory name in which search for matches. 
    boundary_in and boundary_out: give part of the file to consider. Values false by default = parse the whole file.
    output_file = True => the output file given is the one in which the match has been found
    output_file = False => no output file
    """
    #print("++++++++++ input ++++++++++")
    #print(key)
    #print(target)
    
    temp_output = np.array(["name","path"],dtype='U200')

    
    if os.path.isdir(target):
        for path, subdir_list, file_list in os.walk(target):
            for file in file_list:
                file_path = path + "/" + file
                if np.size(key) == 1:
                    key_to_match = key
                    file_match = get_match(key_to_match,file_path)
                    if file_match:
                        if output_file:
                            for match in file_match:
                                temp_output = np.vstack([temp_output, [match, file_path]])
                        else:
                            for match in file_match:
                                temp_output = np.vstack([temp_output])

                elif np.size(key) == 2:
                    key_to_match = [key[0],key[1]]
                    file_match = get_match(key_to_match,file_path)
                    if file_match:
                        if output_file:
                            temp_output = np.vstack([temp_output,[key[1], file_path]])
                        else:
                            temp_output = np.vstack([temp_output])
    elif os.path.isfile(target):
        if np.size(key) == 1:
            key_to_match = key
            file_match = get_match(key_to_match,target)
            if file_match:
                if output_file:
                    for match in file_match:
                        temp_output = np.vstack([temp_output, [match, target]])
                else:
                    for match in file_match:
                        temp_output = np.vstack([temp_output, match])

        elif np.size(key) == 2:
            key_to_match = [key[0],key[1]]
            file_match = get_match(key_to_match,target)
            if file_match:
                if output_file:
                    temp_output = np.vstack([temp_output, [key[1], target]])
                else:
                    temp_output = np.vstack([temp_output, key[1]])
    else:
        print("---------------------------------------------------------------")
        print("ERROR: ", target, " isn't a path or a directory.")
        print("---------------------------------------------------------------")
        sys.exit()   


    if not 'output' in locals():
        output = temp_output
        del temp_output

    #print("++++++++++ output ++++++++++")
    #print(output)
    return output



def is_fortran_extension_file(path):
    match = re.search("(\w+.f90)", path, re.IGNORECASE)
    if match:
        return match[0]
    else:
        return False


