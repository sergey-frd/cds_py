#!/usr/bin/python
#

import getopt, fnmatch, string, glob
import sys
import re
import os
import subprocess
import csv
import time
import shutil
#-------------------------------------------------------------------------------
import sqlite3
import sqlite3 as lite

##from xlwt import Workbook,easyxf

import   getopt, fnmatch, string, glob, subprocess
import commands

import time

import filecmp
import os.path
import shutil

import getopt, time
import ConfigParser

import json

from pprint              import *


import random
#from random import randint
import math
#-------------------------------------------------------------------------------
#
#########################################################################################

def load_nb_us_ds(\
        data,\
        con,\
        cur\
        ):

    DB_TABLE = 'User_Neighb_Ds'
    data['P_User_Neighb_Ds'] = dict() 

    with con:
        con.row_factory = lite.Row
        cur = con.cursor()    

        cur.execute("SELECT  \
            User_Neighb_Ds.ID_User,\
            User_Neighb_Ds.ID_Country,\
            User_Neighb_Ds.ID_City,\
            User_Neighb_Ds.ID_Neighborhoods,\
            User_Neighb_Ds.ID_Digital_Signage,\
            User_Neighb_Ds.ID_Owner,\
            User_Neighb_Ds.Neighborhood,\
            User_Neighb_Ds.Nic_User,\
            User_Neighb_Ds.Dig_Sign,\
            User_Neighb_Ds.DS_Cost,\
            User_Neighb_Ds.DS_Perc_Quality,\
            User_Neighb_Ds.Owner_Name \
            FROM User_Neighb_Ds ")

        con.commit()

        rows = cur.fetchall()

        nn=0
        for line in rows:
            nn=nn+1

            ti_key = \
                line["ID_User"]+','+ \
                line["ID_Country"]+','+ \
                line["ID_City"]+','+ \
                line["ID_Neighborhoods"]+','+ \
                line["ID_Digital_Signage"]+','+ \
                line["ID_Owner"]

            ti_val = \
                line["ID_User"]+','+ \
                line["ID_Country"]+','+ \
                line["ID_City"]+','+ \
                line["ID_Neighborhoods"]+','+ \
                line["ID_Digital_Signage"]+','+ \
                line["ID_Owner"]+','+ \
                line["Neighborhood"]+','+ \
                line["Nic_User"]+','+ \
                line["Dig_Sign"]+','+ \
                line["DS_Cost"]+','+ \
                line["DS_Perc_Quality"]+','+ \
                line["Owner_Name"]

            data['P_User_Neighb_Ds'][ti_key] = ti_val 
