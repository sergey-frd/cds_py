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

from cdb_optim_lib            import *

#-------------------------------------------------------------------------------

########################################################################################

def gen_Nb_Ds_Ti(data, con, cur): 

    DB_TABLE = 'Neighb_Ds_Ti'
    data['Neighb_Ds_Ti'] = dict()  

    columns= []

    columns.append('ID_Country')
    columns.append('ID_City')
    columns.append('ID_Neighborhoods')
    columns.append('ID_Digital_Signage')
    columns.append('ID_Owner')
    columns.append('ID_Time_Interval')
    columns.append('Neighborhood')
    columns.append('Dig_Sign')
    columns.append('Owner_Name')
    columns.append('DS_Cost')
    columns.append('DS_Perc_Quality')
    columns.append('TI_Price')
    columns.append('DS_TI_Price')
    columns.append('TI_D_Sign_People')
    columns.append('TI_Slots')
    columns.append('TI_Slots_Busy')
    columns.append('TI_Slots_Free')
    columns.append('TI_List_Prices')


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
    Time_Interval_Counter = data['Base']['Time_Interval_Counter']

    Time_Slot_Busy_Pers = data['Base']['Time_Slot_Busy_Pers']

    ID_Country = data['Base']['ID_Test_Country']
    ID_City = data['Base']['ID_Test_City']

    undm_keys= data['User_Neighb_Ds_Md'].keys()
    undm_keys.sort()

    uu = 0
    for undm in undm_keys:
        uu += 1

        #ID_User = str(us)
        undm_list = undm.split(',')

        ID_User            = undm_list[0]
        ID_User_Media      = undm_list[1]
        ID_Country         = undm_list[2]
        ID_City            = undm_list[3]
        ID_Neighborhoods   = undm_list[4]
        ID_Digital_Signage = undm_list[5]

        User_Neighb_list = data['User_Neighb_Ds_Md'][undm]

        ID_User             = User_Neighb_list[0]
        ID_User_Media       = User_Neighb_list[1]
        ID_Country          = User_Neighb_list[2]
        ID_City             = User_Neighb_list[3]
        ID_Neighborhoods    = User_Neighb_list[4]
        ID_Digital_Signage  = User_Neighb_list[5]
        ID_Owner            = User_Neighb_list[6]
        Neighborhood        = User_Neighb_list[7]
        Nic_User            = User_Neighb_list[8]
        Dig_Sign            = User_Neighb_list[9]
        Owner_Name          = User_Neighb_list[10]
        DS_Cost             = User_Neighb_list[11]
        DS_Perc_Quality     = User_Neighb_list[12]
        Media_Name          = User_Neighb_list[13]
        Media_Cost          = User_Neighb_list[14]
        Media_Slots         = User_Neighb_list[15]
        Media_Total_Slots   = User_Neighb_list[16]
        
        #print undm,'=>',User_Neighb_list 
        #print 'Media_Name=',Media_Name 
                                       
        d = 0
        for d in xrange(1, Time_Interval_Counter + 1):


            ID_Time_Interval = str(d)

            usdmt_key =\
                ID_Country +','+\
                ID_City  +','+\
                ID_Neighborhoods +','+\
                ID_Digital_Signage +','+\
                ID_Time_Interval

            if data['Neighb_Ds_Ti'].has_key(usdmt_key):
                #print 'found in Neighb_Ds_Ti usd_key=',usdmt_key
                continue

            ti_val = data['Time_Interval'][ID_Time_Interval]
            ti_list = ti_val.split(',')

            TI_Price          = ti_list[0]
            #TI_D_Sign_People = ti_list[1]
            TI_D_Sig_Ppl_Base = ti_list[1]
            TI_Slots          = ti_list[2]

            if random.randint( 0,1)  == 0:
                TI_Slots_Busy = int(TI_Slots)*Time_Slot_Busy_Pers/100
            else:
                TI_Slots_Busy = random.randint( 1,int(TI_Slots) - 5) 

            TI_Slots_Busy = random.randint( 1,int(TI_Slots) - 5) 
            #TI_Slots_Busy = 0

            TI_Slots_Free = int(TI_Slots) - TI_Slots_Busy

            ds = \
                ID_Country +','+ \
                ID_City +','+ \
                ID_Neighborhoods +','+ \
                ID_Digital_Signage

            Dig_Sign_List = data['Digital_Signage'][ds].split(',')
            Dig_Sign        = Dig_Sign_List[0]
            DS_Cost         = int(Dig_Sign_List[1])
            DS_Perc_Quality = int(Dig_Sign_List[2])


            #ds_um_key =\
            #    ID_User +','+\
            #    ID_User_Media +','+\
            #    ID_Country +','+\
            #    ID_City  +','+\
            #    ID_Neighborhoods

            ds_um_key =\
                ID_User +','+\
                ID_User_Media

            UM_DS_COST = int(data['User_Md_Ds_Distrib'][ds_um_key])
            if UM_DS_COST > 0:
                DS_Cost_Perc = DS_Cost * 100 / UM_DS_COST
            else:
                DS_Cost_Perc = 100

            DS_Media_Cost          = int(Media_Cost)        * DS_Cost_Perc /100     
            DS_Media_Total_Slots   = int(Media_Total_Slots) * DS_Cost_Perc /100

            DS_TI_Price  = (int(TI_Price)*DS_Perc_Quality/100)
            #DS_TI_Price  = (int(TI_Price) * DS_Cost_Perc /100)/10*10

            TI_D_Sign_People = (int(TI_D_Sig_Ppl_Base)*DS_Perc_Quality/100)

            ti_dict = Get_Ti_Price(data,\
                int(ID_Time_Interval),\
                DS_TI_Price,\
                int(TI_Slots))

            TI_List_Prices = ''

            for t in xrange(1, int(TI_Slots) ):
                TI_List_Prices += str(round(ti_dict[t],3)) + ';'

            nn += 1

            tuprow = []
            str_nn = str(nn)

            tuprow.append(ID_Country)       
            tuprow.append(ID_City)          
            tuprow.append(ID_Neighborhoods) 
            tuprow.append(ID_Digital_Signage) 
            tuprow.append(ID_Owner) 
            tuprow.append(ID_Time_Interval) 

            tuprow.append(Neighborhood)
            tuprow.append(Dig_Sign)
            tuprow.append(Owner_Name)

            tuprow.append(str(DS_Cost))          
            tuprow.append(str(DS_Perc_Quality)) 

            #tuprow.append(str(DS_Cost_Perc)) 

            tuprow.append(TI_Price)          
            tuprow.append(str(DS_TI_Price))          
            tuprow.append(TI_D_Sign_People)          
            tuprow.append(TI_Slots)  
                    
            tuprow.append(str(TI_Slots_Busy))          
            tuprow.append(str(TI_Slots_Free))    
                  
            tuprow.append(TI_List_Prices)  

            tup.append(tuple(tuprow))
            data['Neighb_Ds_Ti'][usdmt_key] = tuple(tuprow)  
            #print uu,d,UsNb_key,'=>',tuple(tuprow) 

    con.executemany(insQuery, tup)
    con.commit()

