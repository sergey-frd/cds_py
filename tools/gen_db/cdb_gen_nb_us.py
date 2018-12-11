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

def load_Media(data, con, cur): 

    data['Media'] = dict()  

    with con:
        con.row_factory = lite.Row
        cur = con.cursor()    

        cur.execute("SELECT  \
            Media.ID_Media, \
            Media.Type_Media,   \
            Media.Slots   \
            FROM Media ")

        con.commit()

        rows = cur.fetchall()

        nn=0
        for line in rows:
            nn=nn+1

            data['Media'][line["ID_Media"]] = \
                line["Type_Media"] + ',' +\
                line["Slots"]


########################################################################################

def load_User(data, con, cur): 

    data['User'] = dict()  

    User_Counter = data['Base']['User_Counter']
    with con:
        con.row_factory = lite.Row
        cur = con.cursor()    

        cur.execute("SELECT  \
            User.ID_User, \
            User.Nic_User   \
            FROM User ")

        con.commit()

        rows = cur.fetchall()

        nn=0
        for line in rows:
            nn=nn+1

            data['User'][line["ID_User"]] = line["Nic_User"] 
            if nn > User_Counter:
                break


########################################################################################

def gen_User_Nb(data, con, cur): 

    DB_TABLE = 'User_Neighb'
    data['User_Neighb'] = dict()  

    columns= []
    columns.append('ID_User')
    columns.append('ID_Country')
    columns.append('ID_City')
    columns.append('ID_Neighborhoods')
    columns.append('Neighborhood')
    columns.append('Nic_User')

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

    us_keys= data['User'].keys()
    us_keys.sort()


    Neighborhoods_Counter = data['Base']['Neighborhoods_Counter']

    ID_Country = data['Base']['ID_Test_Country']
    ID_City = data['Base']['ID_Test_City']

    uu = 0
    #s = range(1,Neighborhoods_Counter )
    for us in us_keys:
        uu += 1
        ID_User = str(us)
        Nic_User = data['User'][us]

        #print uu,ID_User,'=>',Nic_User

        if random.randint( 0,1)  == 0:
            nb_loop = random.randint( 1,Neighborhoods_Counter-1) 
        else:
            nb_loop = Neighborhoods_Counter-1

        s = range(1,Neighborhoods_Counter )
        d = 0
        for d in xrange(1, nb_loop + 1):

        #
        #    if random.randint( 0,1)  == 0:
        #        if len(s)<2:
        #            continue
        #        nb = s[random.randint(1,len(s))-1]
        #        s.remove(nb)
        #    else:
        #        nb = d

            if len(s)<2:
                continue
            nb = s[random.randint(1,len(s))-1]
            s.remove(nb)

            ID_Neighborhoods = str(nb)

            k =\
                ID_Country +','+\
                ID_City  +','+\
                ID_Neighborhoods

            UsNb_key = \
                ID_User+','+\
                ID_Country +','+\
                ID_City  +','+\
                ID_Neighborhoods


            if data['User_Neighb'].has_key(UsNb_key):
                #print 'found in User_Neighb UsNb_key=',UsNb_key
                continue

            if not data['Neighborhood'].has_key(k):
                #print 'not found in Neighborhood k=',k
                continue

            #k = data['Neighborhood_Dict'][str(nb)] 

            Neighborhood = data['Neighborhood'][k]
            #print uu,d,ID_User,'=>',Nic_User,k,'=>',Neighborhood

            #nb_list = k.split(',')
            #
            #ID_Country       = nb_list[0]
            #ID_City          = nb_list[1]
            #ID_Neighborhoods = nb_list[2]

            nn += 1

            tuprow = []
            str_nn = str(nn)



            tuprow.append(ID_User) 
            tuprow.append(ID_Country)       
            tuprow.append(ID_City)          
            tuprow.append(ID_Neighborhoods) 
            tuprow.append(Neighborhood)
            tuprow.append(Nic_User)
             
            tup.append(tuple(tuprow))
            data['User_Neighb'][UsNb_key] = tuple(tuprow)  
            #print uu,d,UsNb_key,'=>',tuple(tuprow) 

    con.executemany(insQuery, tup)
    con.commit()


