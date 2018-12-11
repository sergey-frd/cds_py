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

def load_nb_us_ds_md_ti(\
        data,\
        con,\
        cur\
        ):

    DB_TABLE = 'User_Neighb_Ds_Md_Ti'
    data['P_User_Neighb_Ds_Md_Ti'] = dict() 

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
            User_Neighb_Ds_Md_Ti.Media_Slots,\
            User_Neighb_Ds_Md_Ti.Media_Total_Slots,\
            User_Neighb_Ds_Md_Ti.DS_Cost,\
            User_Neighb_Ds_Md_Ti.DS_Perc_Quality,\
            User_Neighb_Ds_Md_Ti.UM_DS_COST,\
            User_Neighb_Ds_Md_Ti.DS_Cost_Perc,\
            User_Neighb_Ds_Md_Ti.DS_Media_Cost,\
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
                line["Media_Total_Slots"]+','+ \
                line["DS_Cost"]+','+ \
                line["DS_Perc_Quality"]+','+ \
                line["UM_DS_COST"]+','+ \
                line["DS_Cost_Perc"]+','+ \
                line["DS_Media_Cost"]+','+ \
                line["DS_Media_Total_Slots"]

            data['P_User_Neighb_Ds_Md_Ti'][ti_key] = ti_val 



#########################################################################################
def load_nb_ds_ti(\
        data,\
        con,\
        cur\
        ):

    DB_TABLE = 'Neighb_Ds_Ti'
    data['P_Neighb_Ds_Ti'] = dict() 

    with con:
        con.row_factory = lite.Row
        cur = con.cursor()    

        cur.execute("SELECT  \
            Neighb_Ds_Ti.ID_Country,\
            Neighb_Ds_Ti.ID_City,\
            Neighb_Ds_Ti.ID_Neighborhoods,\
            Neighb_Ds_Ti.ID_Digital_Signage,\
            Neighb_Ds_Ti.ID_Owner,\
            Neighb_Ds_Ti.ID_Time_Interval,\
            Neighb_Ds_Ti.Neighborhood,\
            Neighb_Ds_Ti.Dig_Sign,\
            Neighb_Ds_Ti.Owner_Name,\
            Neighb_Ds_Ti.DS_Cost,\
            Neighb_Ds_Ti.DS_Perc_Quality,\
            Neighb_Ds_Ti.TI_Price,\
            Neighb_Ds_Ti.DS_TI_Price,\
            Neighb_Ds_Ti.TI_D_Sign_People,\
            Neighb_Ds_Ti.TI_Slots,\
            Neighb_Ds_Ti.TI_Slots_Busy,\
            Neighb_Ds_Ti.TI_Slots_Free,\
            Neighb_Ds_Ti.TI_List_Prices \
            FROM Neighb_Ds_Ti ")

        con.commit()

        rows = cur.fetchall()

        nn=0
        for line in rows:
            nn=nn+1

            usdmt_key =\
                line["ID_Country"] +','+\
                line["ID_City"] +','+\
                line["ID_Neighborhoods"] +','+\
                line["ID_Digital_Signage"] +','+\
                line["ID_Time_Interval"]


            ti_val = \
                line["ID_Country"] +','+\
                line["ID_City"] +','+\
                line["ID_Neighborhoods"] +','+\
                line["ID_Digital_Signage"] +','+\
                line["ID_Owner"]+','+ \
                line["ID_Time_Interval"] +','+\
                line["Neighborhood"]+','+ \
                line["Dig_Sign"]+','+ \
                line["Owner_Name"]+','+ \
                line["DS_Cost"]+','+ \
                line["DS_Perc_Quality"]+','+ \
                line["TI_Price"]+','+ \
                line["DS_TI_Price"]+','+ \
                line["TI_D_Sign_People"]+','+ \
                line["TI_Slots"]+','+ \
                line["TI_Slots_Busy"]+','+ \
                line["TI_Slots_Free"]+','+ \
                line["TI_List_Prices"]

            data['P_Neighb_Ds_Ti'][usdmt_key] = ti_val 


