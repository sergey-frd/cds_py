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

def load_us_md(\
        data,\
        con,\
        cur\
        ):

    DB_TABLE = 'User_Neighb_Ds_Md'
    data['User_Md'] = dict() 

    with con:
        con.row_factory = lite.Row
        cur = con.cursor()    

        cur.execute("SELECT  \
            User_Neighb_Ds_Md.ID_User,\
            User_Neighb_Ds_Md.ID_User_Media,\
            User_Neighb_Ds_Md.Media_Name,\
            User_Neighb_Ds_Md.Media_Cost,\
            User_Neighb_Ds_Md.Media_Slots \
            FROM User_Neighb_Ds_Md ")

        con.commit()

        rows = cur.fetchall()

        nn=0
        for line in rows:
            nn=nn+1

            ti_key = \
                line["ID_User"]+','+ \
                line["ID_User_Media"]

            ti_val = \
                line["ID_User_Media"]+','+ \
                line["Media_Name"]+','+ \
                line["Media_Cost"]+','+ \
                line["Media_Slots"]

            #ti_val = \
            #    line["ID_User"]+','+ \
            #    line["ID_User_Media"]+','+ \
            #    line["Media_Name"]

            if not data['User_Md'].has_key(ti_key):
                data['User_Md'][ti_key] =  ti_val

########################################################################################

def gen_User_Media(data, con, cur): 

    #data['User_Media'] = dict()  

    DB_TABLE = 'User_Media'

    columns= []
    columns.append('ID_User_Media')
    columns.append('ID_User')
    columns.append('Media_Name')
    columns.append('Media_Cost')
    columns.append('Media_Slots')

    query_d = 'drop table if exists ' + DB_TABLE
    con.execute(query_d)
    con.commit()

    query = 'CREATE TABLE ' + DB_TABLE + '(ID INTEGER PRIMARY KEY AUTOINCREMENT'
    for col in columns:
        query += ', '+ col + ' TEXT'
    query += ');'
    con.execute(query)

    insQuery1 = 'INSERT INTO ' + DB_TABLE + '('
    insQuery2 = ''
    for col in columns:
        insQuery1 += col + ', '
        insQuery2 += '?, '
    insQuery1 = insQuery1[:-2] + ') VALUES('
    insQuery2 = insQuery2[:-2] + ')'
    insQuery = insQuery1 + insQuery2

    User_Clip_Counter = data['Base']['User_Clip_Counter']



    nn = 0
    tup = []

    um_keys= data['User_Md'].keys()
    um_keys.sort()

    for um in um_keys:


        um_list =  um.split(',')
        ID_User       = um_list[0]
        ID_User_Media = um_list[1]

        um_list =  data['User_Md'][um].split(',')
        ID_User_Media = um_list[0]
        Media_Name    = um_list[1]
        Media_Cost    = um_list[2]
        Media_Slots   = um_list[3]

        nn += 1

        tuprow = []

        tuprow.append(str(ID_User_Media))
        tuprow.append(str(ID_User))
        tuprow.append(Media_Name)       
        tuprow.append(str(Media_Cost))
        tuprow.append(str(Media_Slots))


        #data['User_Media'][ID_User_Media] = tuple(tuprow)  

        tup.append(tuple(tuprow))

    con.executemany(insQuery, tup)
    con.commit()

