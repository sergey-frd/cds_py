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

########################################################################################

def gen_User_Nb_Ds_Md(data, con, cur): 

    DB_TABLE = 'User_Neighb_Ds_Md'
    data['User_Md'] = dict() 

    data['User_Neighb_Ds_Md'] = dict()  

    data['User_Md_Ds_Distrib'] = dict()  
    #data['User_Md_Ds_Cost'] = dict()  

    columns= []
    columns.append('ID_User')
    columns.append('ID_User_Media')

    columns.append('ID_Country')
    columns.append('ID_City')
    columns.append('ID_Neighborhoods')
    columns.append('ID_Digital_Signage')
    columns.append('ID_Owner')

    columns.append('Neighborhood')
    columns.append('Nic_User')
    columns.append('Dig_Sign')
    columns.append('Owner_Name')

    columns.append('DS_Cost')
    columns.append('DS_Perc_Quality')

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

    nn = 0
    tup = []

    und_keys= data['User_Neighb_Ds'].keys()
    und_keys.sort()

    User_Clip_Counter = data['Base']['User_Clip_Counter']
    D_Sign_Counter = data['Base']['D_Sign_Counter']

    ID_Country = data['Base']['ID_Test_Country']
    ID_City = data['Base']['ID_Test_City']

    uu = 0
    for und in und_keys:
        uu += 1

        #ID_User = str(us)
        und_list = und.split(',')

        ID_User            = und_list[0]
        ID_Country         = und_list[1]
        ID_City            = und_list[2]
        ID_Neighborhoods   = und_list[3]
        ID_Digital_Signage = und_list[4]

        User_Neighb_list = data['User_Neighb_Ds'][und]

        ID_User             = User_Neighb_list[0]
        ID_Country          = User_Neighb_list[1]
        ID_City             = User_Neighb_list[2]
        ID_Neighborhoods    = User_Neighb_list[3]
        ID_Digital_Signage  = User_Neighb_list[4]
        ID_Owner            = User_Neighb_list[5]
        Neighborhood        = User_Neighb_list[6]
        Nic_User            = User_Neighb_list[7]
        Dig_Sign           = User_Neighb_list[8]
        DS_Cost             = User_Neighb_list[9]
        DS_Perc_Quality     = User_Neighb_list[10]
        Owner_Name          = User_Neighb_list[11]

        #print und,'=>',User_Neighb_list 
        #print 'Owner_Name=',Owner_Name 

        ID_User_Media = str(int(ID_User) * 1000 + 1 )

        if random.randint( 0,2)  != 0:
            nb_loop = random.randint( 1,User_Clip_Counter-1) 
        else:
            nb_loop = User_Clip_Counter-1

        s = range(1,User_Clip_Counter )
        d = 0
        for d in xrange(1, nb_loop + 1):

            if len(s)<2:
                continue
            um = s[random.randint(1,len(s))-1]
            s.remove(um)

            nn += 1

            if random.randint( 0,1)  == 1:
                ID_User_Media = str(int(ID_User) * 1000 + nn )

            #ID_User_Media=str(\
            #    int(ID_User)*1000 +\
            #    int(ID_Country) +\
            #    int(ID_City) +\
            #    int(ID_Neighborhoods) +\
            #    int(ID_Digital_Signage)\
            #    )


            Media_Name = data['User'][ID_User] +\
                '_Clip_'+ str(int(ID_User_Media) - int(ID_User) * 1000)

            um_key =\
                ID_User  +','+\
                Media_Name

            if not data['User_Md'].has_key(um_key):

                Media_Slots = random.randint(\
                    1,\
                    5,\
                    )

                Media_Cost = random.randint(\
                    data['Base']['Clip_Budget_Min'],\
                    data['Base']['Clip_Budget_Max'],\
                    )*1000

                Media_Total_Slots = str(Media_Cost/100/Media_Slots +1)

                um_val =\
                    Media_Name +','+\
                    str(Media_Cost) +','+\
                    str(Media_Slots) +','+\
                    str(Media_Total_Slots)

                data['User_Md'][um_key] = um_val
            else:
                um_val_list = data['User_Md'][um_key].split(',')

                Media_Name        =     um_val_list[0]
                Media_Cost        = int(um_val_list[1])
                Media_Slots       = int(um_val_list[2])
                Media_Total_Slots = int(um_val_list[3])


            usdm_key =\
                ID_User +','+\
                ID_User_Media +','+\
                ID_Country +','+\
                ID_City  +','+\
                ID_Neighborhoods +','+\
                ID_Digital_Signage

            if data['User_Neighb_Ds_Md'].has_key(usdm_key):
                print 'found in User_Neighb_Ds_Md usd_key=',d,usdm_key
                continue

            ds = \
                ID_Country +','+ \
                ID_City +','+ \
                ID_Neighborhoods +','+ \
                ID_Digital_Signage

            Dig_Sign_List = data['Digital_Signage'][ds].split(',')
            Dig_Sign        = Dig_Sign_List[0]
            DS_Cost         = int(Dig_Sign_List[1])
            DS_Perc_Quality = int(Dig_Sign_List[2])

            ds_um_key =\
                ID_User +','+\
                ID_User_Media

            #ds_um_key =\
            #    ID_User +','+\
            #    ID_User_Media +','+\
            #    ID_Country +','+\
            #    ID_City  +','+\
            #    ID_Neighborhoods

            if not data['User_Md_Ds_Distrib'].has_key(ds_um_key):
                data['User_Md_Ds_Distrib'][ds_um_key] =  0

            if data['User_Md_Ds_Distrib'].has_key(ds_um_key):
                data['User_Md_Ds_Distrib'][ds_um_key] +=  DS_Cost
    


            #print 'Owner_Name=',Owner_Name 

            tuprow = []
            str_nn = str(nn)

            tuprow.append(ID_User) 
            tuprow.append(ID_User_Media) 

            tuprow.append(ID_Country)       
            tuprow.append(ID_City)          
            tuprow.append(ID_Neighborhoods) 
            tuprow.append(ID_Digital_Signage) 
            tuprow.append(ID_Owner) 

            tuprow.append(Neighborhood)
            tuprow.append(Nic_User)
            tuprow.append(Dig_Sign)
            tuprow.append(Owner_Name)
    
            tuprow.append(str(DS_Cost))          
            tuprow.append(str(DS_Perc_Quality))  

            tuprow.append(Media_Name)          
            tuprow.append(str(Media_Cost)) 
            tuprow.append(str(Media_Slots)) 
            tuprow.append(str(Media_Total_Slots))             

            tup.append(tuple(tuprow))
            data['User_Neighb_Ds_Md'][usdm_key] = tuple(tuprow)  
            #print usdm_key,'=>',tuple(tuprow) 

    con.executemany(insQuery, tup)
    con.commit()


