#!/usr/bin/python
#

import re
import sys
import os, fnmatch, string
from pprint import *


#######################################################################################
def allFiles(root, patterns='*', single_level=False, yield_folders=False):
    # Expand patterns from semicolon-separated string to list
    patterns = patterns.split(';')
    for path, subdirs, files in os.walk(root, followlinks=True):
        if yield_folders:
            files.extend(subdirs)
        files.sort( )
        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    yield os.path.join(path, name)
                    break
        if single_level:
            break

#######################################################################################
def allDirs(root, patterns):
    patterns = patterns.split(';')
    for path, subdirs, files in os.walk(root):
        subdirs.sort( )
        for name in subdirs:
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    yield os.path.join(path, name)
                    break

#######################################################################################
# Try to create output file 'filename'
#
def openFile2Write(filename):

    folder_path = os.path.dirname(filename)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    try:
        filename_han = open(filename, 'w')
    except IOError:
        print "Error: cannot create output file: " + filename
        exit(1)

    return filename_han

########################################################################################
def get_Dict_Value(dic,value):
    for name in dic:
        if dic[name] == value:
            return name
    return ""
