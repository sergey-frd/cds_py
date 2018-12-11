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
#-------------------------------------------------------------------------------


#########################################################################################
#
#def load_Nb_Ds(\
#        data,\
#        con,\
#        cur\
#        ):
#
#    data['Digital_Signage'] = dict()  
#
#    with con:
#        con.row_factory = lite.Row
#        cur = con.cursor()    
#
#        cur.execute("SELECT  \
#            Digital_Signage.ID_Country, \
#            Digital_Signage.ID_City,   \
#            Digital_Signage.ID_Neighborhoods,   \
#            Digital_Signage.ID_Digital_Signage,   \
#            Digital_Signage.Dig_Sign   \
#            FROM Digital_Signage ")
#
#        con.commit()
#
#        rows = cur.fetchall()
#
#        nn=0
#        for line in rows:
#            nn=nn+1
#
#            #print  nn,\
#            #    line["ID_Country"],\
#            #    line["ID_City"],\
#            #    line["ID_Neighborhoods"],\
#            #    line["Neighborhoods"]
#
#            k = \
#                line["ID_Country"]+','+ \
#                line["ID_City"]+','+ \
#                line["ID_Neighborhoods"]+','+ \
#                line["ID_Digital_Signage"]
#
#            data['Digital_Signage'][k] = line["Dig_Sign"] 
#             
#########################################################################################
#
#def load_Nb(\
#        data,\
#        con,\
#        cur\
#        ):
#
#    data['Neighborhood'] = dict()  
#
#    with con:
#        con.row_factory = lite.Row
#        cur = con.cursor()    
#
#        cur.execute("SELECT  \
#            Neighborhoods.ID_Country, \
#            Neighborhoods.ID_City,   \
#            Neighborhoods.ID_Neighborhoods,   \
#            Neighborhoods.Neighborhoods   \
#            FROM Neighborhoods ")
#
#        con.commit()
#
#        rows = cur.fetchall()
#
#        nn=0
#        for line in rows:
#            nn=nn+1
#
#            #print  nn,\
#            #    line["ID_Country"],\
#            #    line["ID_City"],\
#            #    line["ID_Neighborhoods"],\
#            #    line["Neighborhoods"]
#
#            k = \
#                line["ID_Country"]+','+ \
#                line["ID_City"]+','+ \
#                line["ID_Neighborhoods"]
#
#            data['Neighborhood'][k] = line["Neighborhoods"] 
#             
#########################################################################################
#
#def gen_Nb_Ds(\
#        data,\
#        con,\
#        cur\
#        ):
#
#    DB_TABLE = 'Digital_Signage'
#
#    columns= []
#    columns.append('ID_Country')
#    columns.append('ID_City')
#    columns.append('ID_Neighborhoods')
#    columns.append('ID_Digital_Signage')
#    columns.append('Dig_Sign')
#
#
#
#    query_d = 'drop table if exists ' + DB_TABLE
#    con.execute(query_d)
#    con.commit()
#
#    query = 'CREATE TABLE ' + DB_TABLE + '(ID INTEGER PRIMARY KEY AUTOINCREMENT'
#    for col in columns:
#        query += ', '+ col + ' TEXT'
#    query += ');'
#    con.execute(query)
#
#    insQuery1 = 'INSERT INTO ' + DB_TABLE + '('
#    insQuery2 = ''
#    for col in columns:
#        insQuery1 += col + ', '
#        insQuery2 += '?, '
#    insQuery1 = insQuery1[:-2] + ') VALUES('
#    insQuery2 = insQuery2[:-2] + ')'
#    insQuery = insQuery1 + insQuery2
#
#    D_Sign_Counter = data['Base']['D_Sign_Counter']
#
#    nb_keys= data['Neighborhood'].keys()
#    nb_keys.sort()
#
#    nn = 0
#    tup = []
#    for nb in nb_keys:
#
#        nb_list = nb.split(',')
#        
#        ID_Country       = nb_list[0]
#        ID_City          = nb_list[1]
#        ID_Neighborhoods = nb_list[2]
#
#        for d in xrange(1, D_Sign_Counter + 1):
#
#            nn += 1
#
#            tuprow = []
#            str_nn = str(nn)
#
#            tuprow.append(ID_Country)       
#            tuprow.append(ID_City)          
#            tuprow.append(ID_Neighborhoods) 
#            tuprow.append(str(nn))
#            tuprow.append(data['Neighborhood'][nb]+'_'+str(d))
#
#            tup.append(tuple(tuprow))
#
#    con.executemany(insQuery, tup)
#    con.commit()
#
##
#########################################################################################
#
#def gen_Nb_Ds_Ow(\
#        data,\
#        con,\
#        cur\
#        ):
#
#
#    DB_TABLE = 'Dig_Sign_Owner'
#
#    columns= []
#    columns.append('ID_Country')
#    columns.append('ID_City')
#    columns.append('ID_Neighborhoods')
#    columns.append('ID_Digital_Signage')
#    columns.append('ID_Owner')
#    #columns.append('Owner_Name')
#
#    nb_keys= data['Neighborhood'].keys()
#    nb_keys.sort()
#
#    query_d = 'drop table if exists ' + DB_TABLE
#    con.execute(query_d)
#    con.commit()
#
#    query = 'CREATE TABLE ' + DB_TABLE + '(ID INTEGER PRIMARY KEY AUTOINCREMENT'
#    for col in columns:
#        query += ', '+ col + ' TEXT'
#    query += ');'
#    con.execute(query)
#
#    insQuery1 = 'INSERT INTO ' + DB_TABLE + '('
#    insQuery2 = ''
#    for col in columns:
#        insQuery1 += col + ', '
#        insQuery2 += '?, '
#    insQuery1 = insQuery1[:-2] + ') VALUES('
#    insQuery2 = insQuery2[:-2] + ')'
#    insQuery = insQuery1 + insQuery2
#
#    D_Sign_Counter = data['Base']['D_Sign_Counter']
#
#    nn = 0
#    tup = []
#    for nb in nb_keys:
#
#        nb_list = nb.split(',')
#
#        ID_Country       = nb_list[0]
#        ID_City          = nb_list[1]
#        ID_Neighborhoods = nb_list[2]
#
#        for d in xrange(1, D_Sign_Counter + 1):
#
#            nn += 1
#
#            tuprow = []
#            str_nn = str(nn)
#
#            tuprow.append(ID_Country)       
#            tuprow.append(ID_City)          
#            tuprow.append(ID_Neighborhoods) 
#            tuprow.append(str(nn))
#            tuprow.append(data['Neighborhood'][nb]+'_'+str(d))
#
#            tup.append(tuple(tuprow))
#
#    con.executemany(insQuery, tup)
#    con.commit()
#
##

