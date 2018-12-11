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

from cdb_gen_nb_ds_lib       import *
from cdb_gen_nb_ds_ow_lib    import *

from cdb_gen_nb_us_md        import *

from cdb_gen_nb_us           import *
from cdb_gen_nb_us_ds        import *
from cdb_gen_nb_us_ds_md     import *
from cdb_gen_nb_us_ds_md_ti  import *

from cdb_load_nb_us_ds_md_ti  import *
from cdb_load_nb_us_ds_md     import *
from cdb_load_nb_us_ds        import *
from cdb_load_nb_us           import *
from cdb_load_us_md           import *

from cdb_optim_lib            import *
from cdb_optim_plan_lib       import *
from cdb_timing_lib           import *
from cdb_results_lib           import *


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
    
    
    print "Input_DB =",data['Base']['Input_DB']
    Input_DB = os.path.normpath(data['Base']['Input_DB'])
    
    con = lite.connect(Input_DB)    
    cur = con.cursor()
    
    load_Owner(data, con, cur) 
    load_Nb(data, con, cur) 
    load_Nb_Ds(data, con, cur) 
    load_Media(data, con, cur)
    load_User(data, con, cur) 
    load_Time_Interval(data, con, cur) 

    load_nb_us_ds_md_ti(data, con, cur) 
    load_nb_us_ds_md(data, con, cur) 
    load_nb_us_ds(data, con, cur) 
    load_us_md(data, con, cur) 

    load_nb_ds_ti(data, con, cur) 
    Load_Nb_Ds_Ow(data, con, cur) 

    #print "data[P_User_Neighb_Ds] = "
    #pprint (data['P_User_Neighb_Ds'])

    #print "data[P_User_Neighb_Ds] = "
    #pprint (data['P_User_Neighb_Ds'])

    #print "data[P_User_Neighb_Ds_Md_Ti] = "
    #pprint (data['P_User_Neighb_Ds_Md_Ti'])

    #pprint (data)
    
    #print "data[Base] = "
    #pprint (data['Base'])

    #Get_Price(data,1,1,14)
    #Get_Price(data,1,7,14)
    #Get_Price(data,1,13,14)
    #Get_Price(data,2,1,61)
    #Get_Price(data,2,30,61)
    #Get_Price(data,2,60,61)
    #Get_Price(data,3,1,216)
    #Get_Price(data,3,100,216)
    #Get_Price(data,3,215,216)
    #Get_Price(data,4,1,864)
    #Get_Price(data,4,400,864)
    #Get_Price(data,4,863,864)

    #Optim_Plan(\
    #    data,\
    #    cur,\
    #    max)


    ### Optim_Plan(data, con, cur) 
    ### gen_nb_us_ds_md_ti_detail(data, con, cur) 

    #print "data[User_Md] = "
    #pprint (data['User_Md'])
    #
    #print "data[P_User_Neighb_Ds_Md] = "
    #pprint (data['P_User_Neighb_Ds_Md'])

    #print "----------------"
    #print "data = "
    #pprint (data)


    Load_P_User_Md_Ow_Ds_Ti(data, con, cur)

    Handle_User_Md_Ow_Ds_Ti_Sum(data, con, cur)

    #print "data[Us_Md_Ow_Ds_Ti][1,1001] = "
    #pprint (data['Us_Md_Ow_Ds_Ti']['1,1001'])

    Handle_User_Md_Ow_Ds_Ti_Paid(data, con, cur)

    #print "----------------"
    #print "data[Us_Md_Ow_Ds_Ti][1,1001] = "
    #pprint (data['Us_Md_Ow_Ds_Ti']['1,1001'])


    #print "----------------"
    #print "----------------"
    #print "----------------"
    # 
    #print "data[Us_Md_Ow_Ds_Ti][1,1001][Media_Cost] = "
    #pprint (data['Us_Md_Ow_Ds_Ti']['1,1001']['Media_Cost'])
    #
    #print "----------------"
    #print "data[Us_Md_Ow_Ds_Ti][1,1001][Media_Paid] = "
    #pprint (data['Us_Md_Ow_Ds_Ti']['1,1001']['Media_Paid'])




    #print "----------------"
    #print "data[Us_Md_Ow_Ds_Ti][1,1001][Us_Md_Ow_Sum_R] = "
    #pprint (data['Us_Md_Ow_Ds_Ti']['1,1001']['Us_Md_Ow_Sum_R'])
    #
    #print "----------------"
    #print "data[Us_Md_Ow_Ds_Ti][1,1001][Ow_Ds_Total_Paid] = "
    #pprint (data['Us_Md_Ow_Ds_Ti']['1,1001']['Ow_Ds_Total_Paid'])



    Handle_User_Md_Ow_Results(data, con, cur)
    
    #print "----------------"
    #print "data[Us_Md_Ow_Ds_Ti][1,1001][Media_Res] = "
    #pprint (data['Us_Md_Ow_Ds_Ti']['1,1001']['Media_Res'])

    print "----------------"
    print "data[Dig_Sign_Owner_TiNnUsMd] = "
    pprint (data['Dig_Sign_Owner_TiNnUsMd'])
#-------------------------------------------------------------------------------
# main module stub to prevent auto execute
#

if __name__ == '__main__':
    akaMain(sys.argv)
    sys.exit(0)

