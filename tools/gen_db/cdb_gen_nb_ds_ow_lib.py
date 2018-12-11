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
import math
#-------------------------------------------------------------------------------


########################################################################################

def load_Owner(\
        data,\
        con,\
        cur\
        ):

    data['Owner'] = dict()  

    with con:
        con.row_factory = lite.Row
        cur = con.cursor()    

        cur.execute("SELECT  \
            Owner.ID_Owner, \
            Owner.Owner_Name   \
            FROM Owner ")

        con.commit()

        rows = cur.fetchall()

        nn=0
        for line in rows:
            nn=nn+1

            data['Owner'][line["ID_Owner"]] = line["Owner_Name"] 

########################################################################################

def load_Nb_Ds(\
        data,\
        con,\
        cur\
        ):

    data['Digital_Signage'] = dict()  
    data['Digital_Signage_dict'] = dict()  

    with con:
        con.row_factory = lite.Row
        cur = con.cursor()    

        cur.execute("SELECT  \
            Digital_Signage.ID_Country, \
            Digital_Signage.ID_City,   \
            Digital_Signage.ID_Neighborhoods,   \
            Digital_Signage.ID_Digital_Signage,   \
            Digital_Signage.Dig_Sign,   \
            Digital_Signage.DS_Cost,   \
            Digital_Signage.DS_Perc_Quality   \
            FROM Digital_Signage ")

        con.commit()

        rows = cur.fetchall()

        nn=0
        for line in rows:
            nn=nn+1

            #print  nn,\
            #    line["ID_Country"],\
            #    line["ID_City"],\
            #    line["ID_Neighborhoods"],\
            #    line["Neighborhoods"]

            k = \
                line["ID_Country"]+','+ \
                line["ID_City"]+','+ \
                line["ID_Neighborhoods"]+','+ \
                line["ID_Digital_Signage"]

            data['Digital_Signage_dict'][line["ID_Digital_Signage"]] = k

            data['Digital_Signage'][k] = \
                line["Dig_Sign"] +','+ \
                line["DS_Cost"]+','+ \
                line["DS_Perc_Quality"]
             
#######################################################################################

def gen_Nb_Ds_Ow(\
        data,\
        con,\
        cur\
        ):

    data['Dig_Sign_Owner'] = dict()  

    DB_TABLE = 'Dig_Sign_Owner'

    columns= []
    columns.append('ID_Country')
    columns.append('ID_City')
    columns.append('ID_Neighborhoods')
    columns.append('ID_Digital_Signage')
    columns.append('ID_Owner')
    columns.append('Owner_Name')

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

    Owner_Counter = data['Base']['Owner_Counter']

    Owner_Counter_loop = \
            random.randint(\
                1,\
                Owner_Counter)

    nn = 0
    tup = []

    ds_keys= data['Digital_Signage'].keys()
    ds_keys.sort()

    for ds in ds_keys:

        ds_list = ds.split(',')

        ID_Country         = ds_list[0]
        ID_City            = ds_list[1]
        ID_Neighborhoods   = ds_list[2]
        ID_Digital_Signage = ds_list[3]

        #for d in xrange(1, Owner_Counter_loop):

        nn += 1

        tuprow = []
        str_nn = str(nn)

        ID_Owner = random.randint(\
            1,\
            data['Base']['Owner_Counter'])

        Owner_Name = data['Owner'][str(ID_Owner)]

        tuprow.append(ID_Country)       
        tuprow.append(ID_City)          
        tuprow.append(ID_Neighborhoods) 
        tuprow.append(ID_Digital_Signage) 
        tuprow.append(str(ID_Owner)) 
        tuprow.append(Owner_Name)

        tup.append(tuple(tuprow))

        dso_key = \
            ID_Country +','+ \
            ID_City +','+ \
            ID_Neighborhoods +','+ \
            ID_Digital_Signage

        data['Dig_Sign_Owner'][dso_key] = str(ID_Owner)

    con.executemany(insQuery, tup)
    con.commit()

#

