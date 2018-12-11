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

from pprint                   import *

#-------------------------------------------------------------------------------

#from cdb_gen_lib             import *
from cdb_gen_nb_ds_lib        import *
from cdb_gen_nb_ds_ow_lib     import *

from cdb_gen_nb_us_md         import *

from cdb_gen_nb_us            import *
from cdb_gen_nb_us_ds         import *
from cdb_gen_nb_us_ds_md      import *
from cdb_gen_nb_us_ds_md_ti   import *

from cdb_load_nb_us_ds_md_ti  import *
from cdb_load_nb_us_ds_md     import *
from cdb_load_nb_us_ds        import *
from cdb_load_nb_us           import *
from cdb_load_us_md           import *

from cdb_gen_nb_ds_ti         import *

from cdb_optim_lib            import *
from cdb_optim_plan_lib       import *


#-------------------------------------------------------------------------------

#File C:\Git\ws01\cds\tools\gen_db\cdb_gen_nb_us_ds_md_ti.py
#  47 29:    data['Time_Interval'] = dict()  
#  79 36:    data['User_Neighb_Ds_Md_Ti'] = dict()  
#File C:\Git\ws01\cds\tools\gen_db\cdb_load_us_md.py
#  49 25:    data['User_Md'] = dict() 
#File C:\Git\ws01\cds\tools\gen_db\cdb_load_nb_us_ds_md.py
#  49 35:    data['P_User_Neighb_Ds_Md'] = dict() 
#File C:\Git\ws01\cds\tools\gen_db\cdb_gen_nb_ds_lib.py
#  46 28:    data['Neighborhood'] = dict()  
#  47 34:    #data['Neighborhood_Dict'] = dict()  
#File C:\Git\ws01\cds\tools\gen_db\cdb_gen_nb_us_ds_md.py
#  45 23:    data['User_Md'] = dict() 
#  47 33:    data['User_Neighb_Ds_Md'] = dict()  
#  49 34:    data['User_Md_Ds_Distrib'] = dict()  
#  50 32:    #data['User_Md_Ds_Cost'] = dict()  
#File C:\Git\ws01\cds\tools\gen_db\cdb_gen_nb_ds_ow_lib.py
#  48 21:    data['Owner'] = dict()  
#  77 31:    data['Digital_Signage'] = dict()  
#  78 36:    data['Digital_Signage_dict'] = dict()  
#  129 30:    data['Dig_Sign_Owner'] = dict()  
#File C:\Git\ws01\cds\tools\gen_db\cdb_gen_lib_s1.py
#  44 31:    data['Digital_Signage'] = dict()  
#  88 28:    data['Neighborhood'] = dict()  
#File C:\Git\ws01\cds\tools\gen_db\cdb_gen_nb_us_ds.py
#  45 30:    data['User_Neighb_Ds'] = dict()  
#File C:\Git\ws01\cds\tools\gen_db\cdb_load_nb_us.py
#  48 29:    data['P_User_Neighb'] = dict() 
#File C:\Git\ws01\cds\tools\gen_db\cdb_load_nb_us_ds_md_ti.py
#  49 38:    data['P_User_Neighb_Ds_Md_Ti'] = dict() 
#File C:\Git\ws01\cds\tools\gen_db\cdb_gen_lib.py
#  44 32:#    data['Digital_Signage'] = dict()  
#  88 29:#    data['Neighborhood'] = dict()  
#File C:\Git\ws01\cds\tools\gen_db\cdb_load_nb_us_ds.py
#  49 32:    data['P_User_Neighb_Ds'] = dict() 
#File C:\Git\ws01\cds\tools\gen_db\cdb_gen_nb_us.py
#  44 26:    data['User_Media'] = dict()  
#  136 21:    data['Media'] = dict()  
#  165 20:    data['User'] = dict()  
#  195 27:    data['User_Neighb'] = dict()  

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# main module with import feature
#
def akaMain(argv):

    argc = len(argv)

    i=1

    #CONF_GEN_DB        =sys.argv[i]; i=i+1
    CONF_GEN_DB  = 'c:\\Git\\ws01\\cds\\tools\\gen_db\\gen_db_0.json'

    CONF_GEN_DB   =os.path.normpath(CONF_GEN_DB)

    print "CONF_GEN_DB         : ",CONF_GEN_DB  

    #-----------------------------------------------
    data = ''
    with open(CONF_GEN_DB) as f:
        data = json.load(f)

    #print "----------------"
    #print "data = "
    #pprint (data)

    print "Input_DB =",data['Base']['Input_DB']
    Input_DB = os.path.normpath(data['Base']['Input_DB'])

    con = lite.connect(Input_DB)    
    cur = con.cursor()

    #load_Nb_Ds(data, con, cur) 
    #load_Nb(data, con, cur) 
    #gen_Nb_Ds(data, con, cur) 
    #gen_Nb_Ds_Ow(data, con, cur) 



    load_Owner(data, con, cur) 
    #pprint (data['Owner'])

    load_Nb(data, con, cur) 


    gen_Nb_Ds(data, con, cur) 
    load_Nb_Ds(data, con, cur) 
    gen_Nb_Ds_Ow(data, con, cur) 
    load_Media(data, con, cur)
    load_User(data, con, cur) 

    #print "data[Neighborhood] = "
    #pprint (data['Neighborhood'])

    gen_User_Nb(data, con, cur)

    #print "data[Digital_Signage] = "
    #pprint (data['Digital_Signage'])
    #
    #print "data[User_Neighb] = "
    #pprint (data['User_Neighb'])

    gen_User_Nb_Ds(data, con, cur)

    #print "data[User_Neighb_Ds] = "
    #pprint (data['User_Neighb_Ds'])

    #print "data[User_Neighb_Ds] = "
    #pprint (data['User_Neighb_Ds'])

    #gen_User_Media(data, con, cur) 
    gen_User_Nb_Ds_Md(data, con, cur)
    
    #print "data[User_Neighb_Ds_Md] = "
    #pprint (data['User_Neighb_Ds_Md'])


    load_Time_Interval(data, con, cur) 

    #print "data[Time_Interval] = "
    #pprint (data['Time_Interval'])

    gen_Nb_Ds_Ti(data, con, cur) 
    gen_User_Nb_Ds_Md_Ti(data, con, cur)

    #print "data[User_Neighb_Ds_Md_Ti] = "
    #pprint (data['User_Neighb_Ds_Md_Ti'])

    #print "data[User_Md] = "
    #pprint (data['User_Md'])

    load_nb_us_ds_md_ti(data, con, cur) 
    load_nb_us_ds_md(data, con, cur) 
    load_nb_us_ds(data, con, cur) 
    load_us_md(data, con, cur) 

    gen_User_Media(data, con, cur) 


    #pprint (data)

#-------------------------------------------------------------------------------
# main module stub to prevent auto execute
#

if __name__ == '__main__':
    akaMain(sys.argv)
    sys.exit(0)

