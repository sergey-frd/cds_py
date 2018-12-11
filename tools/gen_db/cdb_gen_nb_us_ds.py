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

def gen_User_Nb_Ds(data, con, cur): 

    DB_TABLE = 'User_Neighb_Ds'
    data['User_Neighb_Ds'] = dict()  

    columns= []
    columns.append('ID_User')
    columns.append('ID_Country')
    columns.append('ID_City')
    columns.append('ID_Neighborhoods')
    columns.append('ID_Digital_Signage')
    columns.append('ID_Owner')
    columns.append('Neighborhood')
    columns.append('Nic_User')
    columns.append('Dig_Sign')
    columns.append('DS_Cost')
    columns.append('DS_Perc_Quality')
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

    nn = 0
    tup = []

    un_keys= data['User_Neighb'].keys()
    un_keys.sort()


    D_Sign_Used_Counter = data['Base']['D_Sign_Used_Counter']

    ID_Country = data['Base']['ID_Test_Country']
    ID_City = data['Base']['ID_Test_City']

    uu = 0
    for un in un_keys:
        uu += 1

        #ID_User = str(us)
        un_list = un.split(',')

        ID_User            = un_list[0]
        ID_Country         = un_list[1]
        ID_City            = un_list[2]
        ID_Neighborhoods   = un_list[3]

        User_Neighb_list = data['User_Neighb'][un]

        #ID_User           = User_Neighb_list[0]
        #ID_Country        = User_Neighb_list[1]
        #ID_City           = User_Neighb_list[2]
        #ID_Neighborhoods  = User_Neighb_list[3]
        Neighborhood      = User_Neighb_list[4]
        Nic_User          = User_Neighb_list[5]

        if random.randint( 0,1)  == 0:
            nb_loop = random.randint( 1,D_Sign_Used_Counter-1) 
        else:
            nb_loop = D_Sign_Used_Counter-1

        s = range(1,D_Sign_Used_Counter )
        d = 0
        for d in xrange(1, nb_loop + 1):

            if len(s)<2:
                continue
            nb = s[random.randint(1,len(s))-1]
            s.remove(nb)

            ID_Digital_Signage = str(nb)

            usd_key =\
                ID_User +','+\
                ID_Country +','+\
                ID_City  +','+\
                ID_Neighborhoods +','+\
                ID_Digital_Signage 

            ds = \
                ID_Country +','+\
                ID_City  +','+\
                ID_Neighborhoods +','+\
                ID_Digital_Signage 

            if data['User_Neighb_Ds'].has_key(usd_key):
                print 'found in User_Neighb_Ds usd_key=',usd_key
                continue

            #if not data['Digital_Signage_dict'].has_key(ID_Digital_Signage):
            #    #print 'not found in Digital_Signage_dict ID_Digital_Signage=',ID_Digital_Signage
            #    continue

            if not data['Digital_Signage'].has_key(ds):
                #print 'not found in Digital_Signage ds=',ds
                continue

            #k= data['Digital_Signage_dict'][ID_Digital_Signage]
            #Dig_Sign= data['Digital_Signage'][ds]
            #print uu,un,ds,'=>',Dig_Sign 

            Dig_Sign_List = data['Digital_Signage'][ds].split(',')
            Dig_Sign        = Dig_Sign_List[0]
            DS_Cost         = int(Dig_Sign_List[1])
            DS_Perc_Quality = int(Dig_Sign_List[2])


            ID_Owner = data['Dig_Sign_Owner'][ds]
            Owner_Name = data['Owner'][ID_Owner]

            nn += 1

            tuprow = []
            str_nn = str(nn)

            tuprow.append(ID_User) 
            tuprow.append(ID_Country)       
            tuprow.append(ID_City)          
            tuprow.append(ID_Neighborhoods) 
            tuprow.append(ID_Digital_Signage) 
            tuprow.append(ID_Owner) 
            tuprow.append(Neighborhood)
            tuprow.append(Nic_User)
            tuprow.append(Dig_Sign)
            tuprow.append(str(DS_Cost))          
            tuprow.append(str(DS_Perc_Quality)) 
            tuprow.append(Owner_Name)
             
            tup.append(tuple(tuprow))
            data['User_Neighb_Ds'][usd_key] = tuple(tuprow)  
            #print uu,d,UsNb_key,'=>',tuple(tuprow) 

    con.executemany(insQuery, tup)
    con.commit()


