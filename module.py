import sys
import os
import re
import parser as pr
import render as rd
import numpy as np


class Module:

    """
    Initialization functions
    """
    def __init__(self, fortree_obj):
    	print("Module")

    def build_tree(self, fortree_obj):
        if(fortree_obj.render_type == "CALL_TREE" or fortree_obj.render_type == "CALL_GRAPH"):
            pass

        print("build tree")
