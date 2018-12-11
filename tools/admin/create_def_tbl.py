#!/usr/bin/python

import re, os, getopt, sys, StringIO
import fnmatch, string
import csv
from pprint import *
import fnmatch, glob, subprocess
import commands
import time
import filecmp
import os.path
import shutil
from lib_py_utils import *

#-------------------------------------------------------------------------------
# main module 
#
def akaMain(argv):

    i=1
    DUMP_FILE   =sys.argv[i]; i=i+1
    DEF_TBL_FILE=sys.argv[i]; i=i+1

    DUMP_FILE   =os.path.normpath(DUMP_FILE)
    DEF_TBL_FILE=os.path.normpath(DEF_TBL_FILE)

    print "DUMP_FILE   : ",DUMP_FILE   
    print "DEF_TBL_FILE: ",DEF_TBL_FILE 

    f_DEF_TBL_FILE = openFile2Write(DEF_TBL_FILE)

    try:
        f_DUMP_FILE = open(DUMP_FILE, 'r')
    except IOError:
        print "Error: cannot open file: " + DUMP_FILE + "\n"
        sys.exit(2)


    DUMP_FILE_list = f_DUMP_FILE.readlines()
    mm=0
    for line in DUMP_FILE_list:
        mm +=1
        if "CREATE TABLE" in line :
            print mm, line
            f_DEF_TBL_FILE.write(line)

    f_DEF_TBL_FILE.close()
    return

#-------------------------------------------------------------------------------
# main module stub to prevent auto execute
#

if __name__ == '__main__':
    akaMain(sys.argv)
    sys.exit(0)

