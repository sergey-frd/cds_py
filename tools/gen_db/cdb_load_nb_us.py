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

from cdb_pck_unp_lib            import *
#-------------------------------------------------------------------------------
#
#########################################################################################
def load_nb_us(\
        data,\
        con,\
        cur\
        ):

    DB_TABLE = 'User_Neighb'
    data['P_User_Neighb'] = dict() 

    with con:
        con.row_factory = lite.Row
        cur = con.cursor()    

        cur.execute("SELECT  \
            User_Neighb.ID_User,\
            User_Neighb.ID_Country,\
            User_Neighb.ID_City,\
            User_Neighb.ID_Neighborhoods,\
            User_Neighb.Neighborhood \
            FROM User_Neighb ")

        con.commit()

        rows = cur.fetchall()

        nn=0
        for line in rows:
            nn=nn+1

            ti_key = \
                line["ID_User"]+','+ \
                line["ID_Country"]+','+ \
                line["ID_City"]+','+ \
                line["ID_Neighborhoods"]

            ti_val = \
                line["ID_User"]+','+ \
                line["ID_Country"]+','+ \
                line["ID_City"]+','+ \
                line["ID_Neighborhoods"]+','+ \
                line["Neighborhood"]

            data['P_User_Neighb'][ti_key] = ti_val 


#-------------------------------------------------------------------------------

def Load_Nb_Ds_Ow(\
        data,\
        con,\
        cur\
        ):

    Time_Interval_Counter = data['Base']['Time_Interval_Counter']
    data['Dig_Sign_Owner'] = dict()  
    data['Dig_Sign_Owner_TiNnUsMd'] = dict()  

    DB_TABLE = 'Dig_Sign_Owner'
    data['P_Dig_Sign_Owner'] = dict() 

    with con:
        con.row_factory = lite.Row
        cur = con.cursor()    

        cur.execute("SELECT  \
            Dig_Sign_Owner.ID_Country,\
            Dig_Sign_Owner.ID_City,\
            Dig_Sign_Owner.ID_Neighborhoods,\
            Dig_Sign_Owner.ID_Digital_Signage,\
            Dig_Sign_Owner.ID_Owner,\
            Dig_Sign_Owner.Owner_Name \
            FROM Dig_Sign_Owner ")

        con.commit()

        rows = cur.fetchall()

        nn=0
        for line in rows:
            nn=nn+1

            Ow_Ds_key = Create_Ow_Ds_key(\
                line["ID_Owner"], \
                line["ID_Country"], \
                line["ID_City"], \
                line["ID_Neighborhoods"], \
                line["ID_Digital_Signage"])

            Ds_key = Create_Ds_key(\
                line["ID_Country"], \
                line["ID_City"], \
                line["ID_Neighborhoods"], \
                line["ID_Digital_Signage"])

            data['P_Dig_Sign_Owner'][Ds_key] = line["ID_Owner"]  
            data['Dig_Sign_Owner_TiNnUsMd'][Ow_Ds_key] = dict() 
            
            d = 0
            for d in xrange(1, Time_Interval_Counter + 1):
                ID_Time_Interval = str(d) 
                data['Dig_Sign_Owner_TiNnUsMd'][Ow_Ds_key][ID_Time_Interval] = list() 


