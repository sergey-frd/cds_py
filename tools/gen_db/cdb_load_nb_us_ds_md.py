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

def load_nb_us_ds_md(\
        data,\
        con,\
        cur\
        ):

    DB_TABLE = 'User_Neighb_Ds_Md_Ti'
    data['P_User_Neighb_Ds_Md'] = dict() 

    with con:
        con.row_factory = lite.Row
        cur = con.cursor()    

        cur.execute("SELECT  \
            User_Neighb_Ds_Md_Ti.ID_User,\
            User_Neighb_Ds_Md_Ti.ID_User_Media,\
            User_Neighb_Ds_Md_Ti.ID_Country,\
            User_Neighb_Ds_Md_Ti.ID_City,\
            User_Neighb_Ds_Md_Ti.ID_Neighborhoods,\
            User_Neighb_Ds_Md_Ti.ID_Digital_Signage,\
            User_Neighb_Ds_Md_Ti.ID_Owner,\
            User_Neighb_Ds_Md_Ti.Neighborhood,\
            User_Neighb_Ds_Md_Ti.Nic_User,\
            User_Neighb_Ds_Md_Ti.Dig_Sign,\
            User_Neighb_Ds_Md_Ti.Owner_Name,\
            User_Neighb_Ds_Md_Ti.Media_Name,\
            User_Neighb_Ds_Md_Ti.Media_Cost,\
            User_Neighb_Ds_Md_Ti.Media_Slots, \
            User_Neighb_Ds_Md_Ti.UM_DS_COST, \
            User_Neighb_Ds_Md_Ti.DS_Cost_Perc, \
            User_Neighb_Ds_Md_Ti.DS_Media_Cost, \
            User_Neighb_Ds_Md_Ti.DS_Media_Total_Slots \
            FROM User_Neighb_Ds_Md_Ti ")

        con.commit()

        rows = cur.fetchall()

        nn=0
        for line in rows:
            nn=nn+1

            ti_key = \
                line["ID_User"]+','+ \
                line["ID_User_Media"]+','+ \
                line["ID_Country"]+','+ \
                line["ID_City"]+','+ \
                line["ID_Neighborhoods"]+','+ \
                line["ID_Digital_Signage"]+','+ \
                line["ID_Owner"]

            ti_val = \
                line["ID_User"]+','+ \
                line["ID_User_Media"]+','+ \
                line["ID_Country"]+','+ \
                line["ID_City"]+','+ \
                line["ID_Neighborhoods"]+','+ \
                line["ID_Digital_Signage"]+','+ \
                line["ID_Owner"]+','+ \
                line["Neighborhood"]+','+ \
                line["Nic_User"]+','+ \
                line["Dig_Sign"]+','+ \
                line["Owner_Name"]+','+ \
                line["Media_Name"]+','+ \
                line["Media_Cost"]+','+ \
                line["Media_Slots"]+','+ \
                line["UM_DS_COST"]+','+ \
                line["DS_Cost_Perc"]+','+ \
                line["Media_Slots"]+','+ \
                line["DS_Media_Cost"]+','+ \
                line["DS_Media_Total_Slots"]

            data['P_User_Neighb_Ds_Md'][ti_key] = ti_val 
