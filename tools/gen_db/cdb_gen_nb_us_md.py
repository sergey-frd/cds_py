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

#######################################################################################

def gen_Nb_Ds_Us_Ow(\
        data,\
        con,\
        cur\
        ):

    DB_TABLE = 'User_Clip_Nb_Ds_Own'

    columns= []
    columns.append('ID_Country')
    columns.append('ID_City')
    columns.append('ID_Neighborhoods')
    columns.append('ID_Digital_Signage')
    columns.append('ID_User_Media')

    columns.append('ID_Owner')
    columns.append('ID_User')
    columns.append('Dig_Sign')
    columns.append('Owner_Name')
    columns.append('Nic_User')
    columns.append('Media_Name')
    columns.append('Media_Cost')
    columns.append('Media_Slots')
    columns.append('Media_Total_Slots')

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

    D_Sign_Counter = data['Base']['D_Sign_Counter']
    D_Sign_Used_Counter = data['Base']['D_Sign_Used_Counter']

    nn = 0
    tup = []

    um_keys= data['User_Media'].keys()
    um_keys.sort()

    for um in um_keys:


        um_list = data['User_Media'][um]

        ID_User_Media     = um_list[0]
        ID_User           = um_list[1]
        Media_Name        = um_list[2]
        Media_Cost        = um_list[3]
        Media_Slots       = um_list[4]
        Media_Total_Slots = um_list[5]


        if random.randint( 0,1)  == 0:
            D_Sign_Counter_loop = random.randint( 1,D_Sign_Counter) 
        else:
            D_Sign_Counter_loop = D_Sign_Counter

        s = range(1,D_Sign_Used_Counter-1)
        Used_Counter = D_Sign_Used_Counter

        for d in xrange(1, D_Sign_Counter_loop + 1):

            if random.randint( 0,1)  == 0:
                #k = random.randint(1,Used_Counter)
                randomindex = random.randint(0,len(s)-1) 
                k = s[randomindex]
                #k = random.choice(s)
                s.remove(k)
            else:
                k = d

            ds = data['Digital_Signage_dict'][str(k)]
            ds_list = data['Digital_Signage'][ds]
            ds_list = ds.split(',')

            ID_Country         = ds_list[0]
            ID_City            = ds_list[1]
            ID_Neighborhoods   = ds_list[2]
            ID_Digital_Signage = ds_list[3]

            #Dig_Sign= data['Digital_Signage'][ds]
            Dig_Sign_List = data['Digital_Signage'][ds].split(',')
            Dig_Sign        = ds_list[0]
            DS_Cost         = ds_list[1]
            DS_Perc_Quality = ds_list[2]

            nn += 1

            tuprow = []
            str_nn = str(nn)

            dso_key = \
                ID_Country+','+ \
                ID_City+','+ \
                ID_Neighborhoods+','+ \
                ID_Digital_Signage

            ID_Owner = data['Dig_Sign_Owner'][dso_key]
            Owner_Name = data['Owner'][str(ID_Owner)]

            Nic_User = data['User'][ID_User]

            tuprow.append(ID_Country)       
            tuprow.append(ID_City)          
            tuprow.append(ID_Neighborhoods) 
            tuprow.append(ID_Digital_Signage)
            tuprow.append(um)
             
            tuprow.append(ID_Owner)       
            tuprow.append(ID_User)       
            tuprow.append(Dig_Sign)       
            tuprow.append(Owner_Name)       
            tuprow.append(Nic_User)       

            tuprow.append(Media_Name)          
            tuprow.append(str(Media_Cost)) 
            tuprow.append(str(Media_Slots)) 
            tuprow.append(str(Media_Total_Slots)) 

            tup.append(tuple(tuprow))

    con.executemany(insQuery, tup)
    con.commit()


