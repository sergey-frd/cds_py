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
from cdb_optim_plan_lib       import *
from cdb_optim_lib            import *


from cdb_pck_unp_lib            import *
from cdb_pck_unp_1_lib          import *

#-------------------------------------------------------------------------------
def Handle_User_Md_Ow_Results(data, con, cur):


    umi_keys = data['User_Md'].keys()
    umi_keys.sort()

    UsNeigDsMd_keys = data['P_User_Neighb_Ds_Md_Ti'].keys()
    UsNeigDsMd_keys.sort()                                 

    usdmt_keys = data['P_Neighb_Ds_Ti'].keys()
    usdmt_keys.sort()

    owner_keys = data['Owner'].keys()
    owner_keys.sort()

    print "----------------"
    n = 0
    for umi_key in umi_keys:
        n += 1
        #print n,"umi_key = ",umi_key
        ID_User,\
        ID_User_Media = Unpack_User_Md_Key(umi_key) 

        umi_val = data['User_Md'][umi_key]

        ID_User_Media ,\
        Media_Name    ,\
        Media_Cost    ,\
        Media_Slots   = Unpack_User_Md_Val(umi_val) 


        f_Media_Cost = float(Media_Cost)

        data['Us_Md_Ow_Ds_Ti'][umi_key]['Media_Res'].append(round(float(data['Us_Md_Ow_Ds_Ti'][umi_key]['Media_Cost'])))
        data['Us_Md_Ow_Ds_Ti'][umi_key]['Media_Res'].append(round(float(data['Us_Md_Ow_Ds_Ti'][umi_key]['Media_Paid'])))
        data['Us_Md_Ow_Ds_Ti'][umi_key]['Media_Res'].append((round(float(data['Us_Md_Ow_Ds_Ti'][umi_key]['Media_Cost'])) -\
                                                             round(float(data['Us_Md_Ow_Ds_Ti'][umi_key]['Media_Paid']))))

        #print "----------------"
        #print  "data[Us_Md_Ow_Ds_Ti][umi_key][Media_Res] = "
        print umi_key,data['Us_Md_Ow_Ds_Ti'][umi_key]['Media_Res']

        Ow_List = data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_List']
        Ow_List.sort()
        for ID_Owner in Ow_List:
            #print "ID_Owner = ",ID_Owner
            
            data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Sum_Res'][ID_Owner].append(round(float(data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Sum_R'][ID_Owner])))
            data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Sum_Res'][ID_Owner].append(round(float(data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Total_Paid'][ID_Owner])))
            data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Sum_Res'][ID_Owner].append((round(float(data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Sum_R'][ID_Owner])) -\
                                                                                  round(float(data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Total_Paid'][ID_Owner]))))
            
            #print "   data[Us_Md_Ow_Ds_Ti][umi_key][Us_Md_Ow_Sum_Res][ID_Owner] = "
            print "   ",umi_key,ID_Owner,data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Sum_Res'][ID_Owner]


            Ow_Ds_List = data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_List'][ID_Owner]
            Ow_Ds_List.sort()
            for Ds_key in Ow_Ds_List:
                #print "Ds_key = ",Ds_key
                
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Sum_Res'][ID_Owner][Ds_key].append(round(float(data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Sum_R'][ID_Owner][Ds_key])))
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Sum_Res'][ID_Owner][Ds_key].append(round(float(data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Paid'][ID_Owner][Ds_key])))
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Sum_Res'][ID_Owner][Ds_key].append((round(float(data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Sum_R'][ID_Owner][Ds_key])) -\
                                                                                      round(float(data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Paid'][ID_Owner][Ds_key]))))
                
                #print "      data[Us_Md_Ow_Ds_Ti][umi_key][Us_Md_Ow_Ds_Sum_Res][ID_Owner][Ds_key] = "
                print "      ",umi_key,ID_Owner,Ds_key,data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Sum_Res'][ID_Owner][Ds_key]

        #-------------------------------------------
        #if n >= 1:
        #    break   

