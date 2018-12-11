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

from cdb_gen_nb_ds_lib          import *
from cdb_gen_nb_ds_ow_lib       import *

from cdb_gen_nb_us_md           import *

from cdb_gen_nb_us              import *
from cdb_gen_nb_us_ds           import *
from cdb_gen_nb_us_ds_md        import *
from cdb_gen_nb_us_ds_md_ti     import *

from cdb_load_nb_us_ds_md_ti    import *

from cdb_pck_unp_lib            import *
from cdb_pck_unp_1_lib          import *
#-------------------------------------------------------------------------------
# 
# Get_Ti_Price(data,4,48,10)
# Get_Ti_Price(data,3,36,20)
# Get_Ti_Price(data,2,24,30)
# Get_Ti_Price(data,1,12,40)
# 
#-------------------------------------------------------------------------------
def Get_Ti_Price(\
    data,\
    ti_type,\
    base,\
    max):

    cur = 1
    ti_dict = dict()

    x = data['Base']['Dig_Sign_Max_Time_Interv_Price']
    koef_min = data['Base']['Dig_Sign_Time_Int_SQR_min']
    koef_max = data['Base']['Dig_Sign_Time_Int_SQR_max']


    koef = koef_max
    
    #koef = 0.6
    
    if ti_type == 1:
        koef = .9
    
    elif ti_type == 2:
        koef = .88
    
    elif ti_type == 3:
        koef = .86
    
    elif ti_type == 4:
        koef = .8

    steps  = max - cur
    res    = x
    result = res

    limit = max * 85/100

    nn = 0
    for i in xrange(1, steps+1):
        nn += 1
        d = max - i

        res = res ** koef

        ti_dict[i] = res + base

    return ti_dict

#-------------------------------------------------------------------------------

# Get_Price(data,4,250,48,1,10)
# Get_Price(data,3,100,36,1,20)
# Get_Price(data,2,30,24,1,30)
# Get_Price(data,1,10,12,1,40)
#-------------------------------------------------------------------------------
def Get_Price(\
    data,\
    ti_type,\
    people,\
    base,\
    cur,\
    max):


    x = data['Base']['Dig_Sign_Max_Time_Interv_Price']
    koef_min = data['Base']['Dig_Sign_Time_Int_SQR_min']
    koef_max = data['Base']['Dig_Sign_Time_Int_SQR_max']


    koef = koef_max
    
    #koef = 0.6
    
    if ti_type == 1:
        koef = .9
    
    elif ti_type == 2:
        koef = .88
    
    elif ti_type == 3:
        koef = .86
    
    elif ti_type == 4:
        koef = .8



    #if ti_type == 1:
    #    koef = .8
    #
    #elif ti_type == 2:
    #    koef = .85
    #
    #elif ti_type == 3:
    #    koef = .87
    #
    #elif ti_type == 4:
    #    koef = .89
    #

    print "---------------"
    steps  = max - cur
    res    = x
    result = res
    

    limit = max * 85/100


    print "ti_type=",ti_type
    print "koef=",koef
    print "limit=",limit

    nn = 0
    for i in xrange(1, steps+1):
        nn += 1
        d = max - i

        #if d < int(limit):
        #    koef = koef_min

            #if ti_type == 1:
            #    koef = koef_min
            #
            #elif ti_type == 2:
            #    koef = .95
            #
            #elif ti_type == 3:
            #    koef = .97
            #
            #elif ti_type == 4:
            #    koef = .99



            #print "koef=",d,koef

        #res = res ** 0.9
        #res = round(res ** koef + base)
        #res = int(res ** koef + base)
        res = res ** koef + base

        people_price = round(people/res,3)
        #people_price = int(people)
        peoples      = int(people_price * base)

        #if max - people_price > 10:
        #    res = res ** data['Base']['Dig_Sign_Time_Interv_SQR']
        #    res = res ** data['Base']['Dig_Sign_Time_Interv_SQR'] - 0.1
        #    people_price = round(people/res,3)



        if max > 100:
            if nn > 5:
                nn = 0
                print d,koef,base,max,people,round(res,3),people_price,peoples
        else:
            print d,koef,base,max,people,round(res,3),people_price,peoples

        result=int(res) + base

    #print "---------------"
    print d,koef,base,max,people,round(res,3),people_price,peoples
    #print "---------------"
    return result

#########################################################################################

def gen_nb_us_ds_md_ti_detail(\
        data,\
        con,\
        cur\
        ):

    print "-------------------"
    print         '4,250,48,1,10'
    Get_Price(data,4,250,48,1,10)


    print "-------------------"
    print         '3,100,36,1,20'
    Get_Price(data,3,100,36,1,20)


    print "-------------------"
    print         '2,30,24,1,30'
    Get_Price(data,2,30,24,1,30)


    print "-------------------"
    print         '1,10,12,1,40'
    Get_Price(data,1,10,12,1,40)

#-------------------------------------------------------------------------------
def Load_P_User_Md_Ow_Ds_Ti(data, con, cur):


    Min_4_Piople_Price = float(data['Base']['Min_4_Piople_Price'])
    Time_Interval_Counter = data['Base']['Time_Interval_Counter']
    Clip_Budget_End   = data['Base']['Clip_Budget_End']
    Clip_Budget_Start = data['Base']['Clip_Budget_Start']


    #print "Clip_Budget_End   = ",Clip_Budget_End  
    #print "Clip_Budget_Start = ",Clip_Budget_Start

    data['Us_Md_Ow_Ds_Ti']= dict()

    umi_keys = data['User_Md'].keys()
    umi_keys.sort()

    UsNeigDsMd_keys = data['P_User_Neighb_Ds_Md_Ti'].keys()
    UsNeigDsMd_keys.sort()                                 

    usdmt_keys = data['P_Neighb_Ds_Ti'].keys()
    usdmt_keys.sort()

    owner_keys = data['Owner'].keys()
    owner_keys.sort()

    n = 0
    for umi_key in umi_keys:
        n += 1

        ID_User,\
        ID_User_Media = Unpack_User_Md_Key(umi_key) 

        umi_val = data['User_Md'][umi_key]

        ID_User_Media ,\
        Media_Name    ,\
        Media_Cost    ,\
        Media_Slots   = Unpack_User_Md_Val(umi_val) 

        #print n,\
        #    ID_User,\
        #    ID_User_Media ,\
        #    Media_Name    ,\
        #    Media_Cost    ,\
        #    Media_Slots

        #data['User_Md_Paid'][umi_key] = 0

        #print "umi_key = ",umi_key

        uu = 0
        for undm_key in UsNeigDsMd_keys:
            uu += 1

            UsNeigDsMd_ID_User            ,\
            UsNeigDsMd_ID_User_Media      ,\
            ID_Country         ,\
            ID_City            ,\
            ID_Neighborhoods   ,\
            ID_Digital_Signage ,\
            ID_Owner           = Unpack_User_Neighb_Ds_Md_Key(undm_key) 

            if   ID_User      != UsNeigDsMd_ID_User       : continue
            elif ID_User_Media!= UsNeigDsMd_ID_User_Media : continue

            Ow_Ds_key = Create_Ow_Ds_key(\
                ID_Owner,
                ID_Country,
                ID_City,
                ID_Neighborhoods,
                ID_Digital_Signage)

            Ds_key = Create_Ds_key(\
                ID_Country,
                ID_City,
                ID_Neighborhoods,
                ID_Digital_Signage)


            if not data['Us_Md_Ow_Ds_Ti'].has_key(umi_key):
                data['Us_Md_Ow_Ds_Ti'][umi_key] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Media_Cost'] = Media_Cost
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Media_Paid'] = 0
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Media_Res'] = list()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Total_Cost'] = 0
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_List'] = list()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_List'] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Total_Cost'] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Total_Paid'] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_List'] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Price'] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Paid'] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Paid_Dict'] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Total_Price'] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Price'] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Paid'] = dict()


            if not ID_Owner in data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_List']:
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_List'].append(ID_Owner)
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_List'][ID_Owner] = list()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Total_Cost'][ID_Owner] = 0
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Total_Paid'][ID_Owner] = 0
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_List'][ID_Owner] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Price'][ID_Owner] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Paid'][ID_Owner] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Paid_Dict'][ID_Owner] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Total_Price'][ID_Owner] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Price'][ID_Owner] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Paid'][ID_Owner] = dict()

            if not Ds_key in data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_List'][ID_Owner]:
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_List'][ID_Owner].append(Ds_key)
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_List'][ID_Owner][Ds_key] = list()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Price'][ID_Owner][Ds_key] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Paid'][ID_Owner][Ds_key] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Paid_Dict'][ID_Owner][Ds_key] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Total_Price'][ID_Owner][Ds_key] = 0


                Ds_Val = data['Digital_Signage'][Ds_key]
                
                Dig_Sign        ,\
                DS_Cost         ,\
                DS_Perc_Quality = Unpack_Ds_Val(Ds_Val)
                
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Price'][ID_Owner][Ds_key] = DS_Cost
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Paid'][ID_Owner][Ds_key] = 0

                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Total_Cost'][ID_Owner] += DS_Cost
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Total_Cost'] += DS_Cost


                iID_Time_Interval = 0
    
                for iID_Time_Interval in xrange(1, Time_Interval_Counter + 1):
    
                    ID_Time_Interval = str(iID_Time_Interval)

                    #undmt_key = \
                    #    undm_key +','+\
                    #    str(ID_Time_Interval)
    
                    data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_List'][ID_Owner][Ds_key].append(ID_Time_Interval)

                    undm_val = data['P_User_Neighb_Ds_Md_Ti'][undm_key]
                    #print uu,undm_key,"=>",undm_val


                    undm_ID_User              ,\
                    undm_ID_User_Media        ,\
                    undm_ID_Country           ,\
                    undm_ID_City              ,\
                    undm_ID_Neighborhoods     ,\
                    undm_ID_Digital_Signage   ,\
                    undm_ID_Owner             ,\
                    Neighborhood              ,\
                    Nic_User                  ,\
                    Dig_Sign                  ,\
                    Owner_Name                ,\
                    Media_Name                ,\
                    Media_Cost                ,\
                    Media_Slots               ,\
                    Media_Total_Slots         ,\
                    DS_Cost                   ,\
                    DS_Perc_Quality           ,\
                    UM_DS_COST                ,\
                    DS_Cost_Perc              ,\
                    DS_Media_Cost             ,\
                    DS_Media_Total_Slots = Unpack_User_Nb__Ds_Md_List(undm_val)

    
                    usdmt_key = Create_Usdmt_Key(\
                        ID_Country,
                        ID_City,
                        ID_Neighborhoods,
                        ID_Digital_Signage,
                        ID_Time_Interval)
    
                    usdmt_val      = data['P_Neighb_Ds_Ti'][usdmt_key]
                    ID_Country         ,\
                    ID_City            ,\
                    ID_Neighborhoods   ,\
                    ID_Digital_Signage ,\
                    ID_Owner           ,\
                    ID_Time_Interval   ,\
                    Neighborhood       ,\
                    Dig_Sign           ,\
                    Owner_Name         ,\
                    DS_Cost            ,\
                    DS_Perc_Quality    ,\
                    TI_Price           ,\
                    TI_D_Sign_People   ,\
                    DS_TI_Price        ,\
                    TI_Slots           ,\
                    TI_Slots_Busy      ,\
                    TI_Slots_Free      ,\
                    TI_List_Prices     = Unpack_Neighb_Ds_Ti_Key(usdmt_val)

                    TI_Prices_list = TI_List_Prices.split(';')


                    i = 0
                    fti = 0

                    data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Price'][ID_Owner][Ds_key][ID_Time_Interval] = 0
                    data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Paid'][ID_Owner][Ds_key][ID_Time_Interval] = 0
                    data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Paid_Dict'][ID_Owner][Ds_key][ID_Time_Interval] = dict()

                    #print "ID_Owner = ",ID_Owner
                    #print "Ds_key = ",Ds_key
                    #print "TI_Slots_Busy = ",TI_Slots_Busy
                    #print "TI_Prices_list = ",TI_Prices_list

                    #for tp in TI_Prices_list:
                    for tp in reversed(TI_Prices_list):

                        i += 1
                        #tpk = int(TI_Slots)-i
                        tpk = i

                        #print tpk,tp

                        if tp == '':
                            continue


                        if int(TI_Slots_Busy) >= tpk:
                            continue

                        fti = round(float(tp),3)
            
                        if Clip_Budget_Start <= fti:
                            break

                        #print '***',tpk,tp
                        data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Price'][ID_Owner][Ds_key][ID_Time_Interval] = fti
                        data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Total_Price'][ID_Owner][Ds_key] += fti

                        #break

        #-------------------------------------------
        #if n >= 1:
        #    break   

    #print "data[Digital_Signage] = "
    #pprint (data['Digital_Signage'])
    
    #print "data[Us_Md_Ow_Ds_Ti] = "
    #pprint (data['Us_Md_Ow_Ds_Ti'])
    
    #print "----------------"
    #print "data[Us_Md_Ow_Ds_Ti][1,1001] = "
    #pprint (data['Us_Md_Ow_Ds_Ti']['1,1001'])

    #print "----------------"
    #print "data[Us_Md_Ow_Ds_Ti][1,1001][Ow_Ds_Ti_Price] = "
    #pprint (data['Us_Md_Ow_Ds_Ti']['1,1001']['Ow_Ds_Ti_Price'])
    #
    #print "----------------"
    #print "data[Us_Md_Ow_Ds_Ti][1,1001][Ow_Ds_Ti_Total_Price] = "
    #pprint (data['Us_Md_Ow_Ds_Ti']['1,1001']['Ow_Ds_Ti_Total_Price'])

#-------------------------------------------------------------------------------
def Handle_User_Md_Ow_Ds_Ti_Sum(data, con, cur):

    Min_4_Piople_Price = float(data['Base']['Min_4_Piople_Price'])
    Time_Interval_Counter = data['Base']['Time_Interval_Counter']
    Clip_Budget_End = data['Base']['Clip_Budget_End']
    Clip_Budget_Start = data['Base']['Clip_Budget_Start']


    umi_keys = data['User_Md'].keys()
    umi_keys.sort()

    UsNeigDsMd_keys = data['P_User_Neighb_Ds_Md_Ti'].keys()
    UsNeigDsMd_keys.sort()                                 

    usdmt_keys = data['P_Neighb_Ds_Ti'].keys()
    usdmt_keys.sort()

    owner_keys = data['Owner'].keys()
    owner_keys.sort()

    n = 0
    for umi_key in umi_keys:
        n += 1
        #print n,"umi_key = ",umi_key
        data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Sum'] = dict()
        data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Sum_R'] = dict()
        data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Sum_Res'] = dict()
        data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Sum'] = dict()
        data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Sum_R'] = dict()
        data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Sum_Res'] = dict()
        data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Ti_Sum'] = dict()
        data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Ti_Sum_R'] = dict()

        ID_User,\
        ID_User_Media = Unpack_User_Md_Key(umi_key) 

        umi_val = data['User_Md'][umi_key]

        ID_User_Media ,\
        Media_Name    ,\
        Media_Cost    ,\
        Media_Slots   = Unpack_User_Md_Val(umi_val) 


        f_Media_Cost = float(Media_Cost)
        #print "f_Media_Cost = ",f_Media_Cost

        Ow_List = data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_List']
        for ID_Owner in Ow_List:
            #print "ID_Owner = ",ID_Owner

            Ow_Ds_Total_Cost = float(data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Total_Cost'][ID_Owner])
            Us_Md_Ow_Ds_Total_Cost = float(data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Total_Cost'])

            Media_Cost_Ow = f_Media_Cost * Ow_Ds_Total_Cost/Us_Md_Ow_Ds_Total_Cost 
            #print "ID_Owner = ",ID_Owner
            #print "Ow_Ds_Total_Cost = ",Ow_Ds_Total_Cost
            #print "Us_Md_Ow_Ds_Total_Cost = ",Us_Md_Ow_Ds_Total_Cost
            #print ID_Owner,"Media_Cost_Ow = ",Media_Cost_Ow
            data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Sum'][Media_Cost_Ow] = ID_Owner
            data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Sum_R'][ID_Owner] = Media_Cost_Ow
            data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Sum_Res'][ID_Owner] = list()
            data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Sum'][ID_Owner] = dict()
            data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Sum_R'][ID_Owner] = dict()
            data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Sum_Res'][ID_Owner] = dict()
            data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Ti_Sum'][ID_Owner] = dict()
            data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Ti_Sum_R'][ID_Owner] = dict()


            Ow_Ds_List = data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_List'][ID_Owner]
            for Ds_key in Ow_Ds_List:
                #print "Ds_key = ",Ds_key

                DS_Cost = data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Price'][ID_Owner][Ds_key]
                f_DS_Cost = float(DS_Cost)
                Media_Cost_Ow_Ds = Media_Cost_Ow * f_DS_Cost/Ow_Ds_Total_Cost 
                #print '   ',ID_Owner,Ds_key,"Media_Cost_Ow_Ds = ",Media_Cost_Ow_Ds
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Sum'][ID_Owner][Media_Cost_Ow_Ds] = Ds_key
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Sum_R'][ID_Owner][Ds_key] = Media_Cost_Ow_Ds
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Sum_Res'][ID_Owner][Ds_key] = list()

                Ow_Ds_Ti_Total_Price = data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Total_Price'][ID_Owner][Ds_key]
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Ti_Sum'][ID_Owner][Ds_key] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Ti_Sum_R'][ID_Owner][Ds_key] = dict()

                iID_Time_Interval = 0
                for iID_Time_Interval in xrange(1, Time_Interval_Counter + 1):
                    ID_Time_Interval = str(iID_Time_Interval)
                    #print "ID_Time_Interval = ",ID_Time_Interval

                    Ow_Ds_Ti_Price = data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Price'][ID_Owner][Ds_key][ID_Time_Interval]
                    #print "Ow_Ds_Ti_Price = ",Ow_Ds_Ti_Price
                    f_Ow_Ds_Ti_Price = float(Ow_Ds_Ti_Price)

                    if Ow_Ds_Ti_Total_Price > 0:
                        Media_Cost_Ow_Ds_Ti = Media_Cost_Ow_Ds * f_Ow_Ds_Ti_Price/Ow_Ds_Ti_Total_Price
                    else:
                        Media_Cost_Ow_Ds_Ti = 0
                     
                    #print '      ',ID_Owner,Ds_key,ID_Time_Interval,"Media_Cost_Ow_Ds_Ti = ",Media_Cost_Ow_Ds_Ti
                    data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Ti_Sum'][ID_Owner][Ds_key][Media_Cost_Ow_Ds_Ti] = ID_Time_Interval
                    data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Ti_Sum_R'][ID_Owner][Ds_key][ID_Time_Interval] = Media_Cost_Ow_Ds_Ti

        #-------------------------------------------
        #if n >= 1:
        #    break   

