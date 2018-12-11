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
def Handle_User_Md_Ow(data, con, cur):



    data['umi_dict']= dict()
    data['User_Neighb_Ds_Md_Dict']= dict()

    Min_4_Piople_Price = float(data['Base']['Min_4_Piople_Price'])
    Time_Interval_Counter = data['Base']['Time_Interval_Counter']
    Clip_Budget_End = data['Base']['Clip_Budget_End']
    Clip_Budget_Start = data['Base']['Clip_Budget_Start']

    umi_keys = data['User_Md'].keys()
    umi_keys.sort()

    n = 0
    for umi_key in umi_keys:
        n += 1

        #umi_dict = dict()
        umi_val = data['User_Md'][umi_key]

        ID_User,\
        ID_User_Media = Unpack_User_Md_Key(umi_key) 

        umi_val = data['User_Md'][umi_key]

        ID_User_Media ,\
        Media_Name    ,\
        Media_Cost    ,\
        Media_Slots   = Unpack_User_Md_Val(umi_val) 


        umiow_list = data['User_Md_Owner_List'][umi_key]
        umiow_list.sort()

        now = 0
        for ID_Owner in umiow_list:
            now += 1


            umiow_list = data['User_Md_Owner_Ds_List'][umi_key][ID_Owner]
            umiow_list.sort()

            nowd = 0
            for Ds_key in umiow_list:
                nowd += 1


#-------------------------------------------------------------------------------
def Handle_User_Md_Ow_Ds_Ti_Paid(data, con, cur):

    Min_4_Piople_Price = float(data['Base']['Min_4_Piople_Price'])
    Time_Interval_Counter = data['Base']['Time_Interval_Counter']
    Clip_Budget_End   = float(data['Base']['Clip_Budget_End'])
    Clip_Budget_Start = float(data['Base']['Clip_Budget_Start'])


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
        print n,"STARTED umi_key = ",umi_key
        ID_User,\
        ID_User_Media = Unpack_User_Md_Key(umi_key) 

        umi_val = data['User_Md'][umi_key]

        ID_User_Media ,\
        Media_Name    ,\
        Media_Cost    ,\
        Media_Slots   = Unpack_User_Md_Val(umi_val) 


        f_Media_Cost = float(Media_Cost)

        Us_Md_Ow_Sum_keys = data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Sum'].keys()
        Us_Md_Ow_Sum_keys.sort(reverse=True)


        #print "Media_Cost = ",Media_Cost

        flag_break = 0
        #-- Owners -----------------------------------------------------
        Delta_Ow = 0
        flag_break_Ow = 0

        nOw = 0
        for Us_Md_Ow_Sum in Us_Md_Ow_Sum_keys:
            nOw += 1

            ID_Owner = data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Sum'][Us_Md_Ow_Sum] 
            #print '   ',ID_Owner,"Us_Md_Ow_Sum = ",Us_Md_Ow_Sum

            print '===',ID_Owner,"Us_Md_Ow_Sum = ",\
                Us_Md_Ow_Sum,'+',Delta_Ow,'=',Us_Md_Ow_Sum + Delta_Ow

            Us_Md_Ow_Sum += Delta_Ow

            Us_Md_Ow_Ds_Sum_keys = data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Sum'][ID_Owner].keys()
            Us_Md_Ow_Ds_Sum_keys.sort(reverse=True)


            #----------------------------------------------------------------  
            Delta_Ds = Delta_Ow
            flag_break_Ds = 0

            nDs = 0
            for Us_Md_Ow_Ds_Sum in Us_Md_Ow_Ds_Sum_keys:
                nDs += 1

                Ds_key = data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Sum'][ID_Owner][Us_Md_Ow_Ds_Sum] 

                #print '      ',ID_Owner,Ds_key,"Us_Md_Ow_Ds_Sum = ",Us_Md_Ow_Ds_Sum
                print '======',ID_Owner,Ds_key,"Us_Md_Ow_Ds_Sum = ",\
                    Us_Md_Ow_Ds_Sum,'+',Delta_Ds,'=',Us_Md_Ow_Ds_Sum + Delta_Ds

                Us_Md_Ow_Ds_Sum += Delta_Ds

                ID_Country           ,\
                ID_City              ,\
                ID_Neighborhoods     ,\
                ID_Digital_Signage   = Unpack_Ds_key(Ds_key)


                Ow_Ds_key = Create_Ow_Ds_key(\
                    ID_Owner,
                    ID_Country,
                    ID_City,
                    ID_Neighborhoods,
                    ID_Digital_Signage)

                undm_key = Create_Usdm_Key(\
                    ID_User      ,
                    ID_User_Media,
                    ID_Country,
                    ID_City,
                    ID_Neighborhoods,
                    ID_Digital_Signage,
                    ID_Owner)

                undm_val = data['P_User_Neighb_Ds_Md_Ti'][undm_key]

                ID_User              ,\
                ID_User_Media        ,\
                ID_Country           ,\
                ID_City              ,\
                ID_Neighborhoods     ,\
                ID_Digital_Signage   ,\
                ID_Owner             ,\
                Neighborhood         ,\
                Nic_User             ,\
                Dig_Sign             ,\
                Owner_Name           ,\
                Media_Name           ,\
                Media_Cost           ,\
                Media_Slots          ,\
                Media_Total_Slots    ,\
                DS_Cost              ,\
                DS_Perc_Quality      ,\
                UM_DS_COST           ,\
                DS_Cost_Perc         ,\
                DS_Media_Cost        ,\
                DS_Media_Total_Slots = Unpack_User_Nb__Ds_Md_List(undm_val)

                Us_Md_Ow_Ds_Ti_Sum_keys = data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Ti_Sum'][ID_Owner][Ds_key].keys()
                Us_Md_Ow_Ds_Ti_Sum_keys.sort(reverse=True)
                #Us_Md_Ow_Ds_Ti_Sum_keys.sort
                # 
                #----------------------------------------------------------------  
                Delta_Ti = Delta_Ds
                len_Us_Md_Ow_Ds_Ti_Sum_keys = len(Us_Md_Ow_Ds_Ti_Sum_keys)
                nTi = 0

                for Media_Cost_Ow_Ds_Ti in Us_Md_Ow_Ds_Ti_Sum_keys:
                    nTi += 1
                    ID_Time_Interval = data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Ti_Sum'][ID_Owner][Ds_key][Media_Cost_Ow_Ds_Ti] 



                    #print '         ',ID_Owner,Ds_key,ID_Time_Interval,"Media_Cost_Ow_Ds_Ti = ",Media_Cost_Ow_Ds_Ti
                    print '=========',ID_Owner,Ds_key,ID_Time_Interval,"Media_Cost_Ow_Ds_Ti = ",\
                        Media_Cost_Ow_Ds_Ti,'+',Delta_Ti,'=',Media_Cost_Ow_Ds_Ti + Delta_Ti

                    #print '***',ID_Owner,Ds_key,ID_Time_Interval,"Media_Cost_Ow_Ds_Ti = ",Media_Cost_Ow_Ds_Ti
                    Media_Cost_Ow_Ds_Ti += Delta_Ti

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

                    i_TI_Slots_Busy = int(TI_Slots_Busy)

                    TI_Prices_list = TI_List_Prices.split(';')

                    tMedia_Cost   =  Media_Cost_Ow_Ds_Ti
                    Paid   =  0
                    i = 0
                    DsTiNnUsMd_Key = ''
                    #for tp in TI_Prices_list:
                    for tp in reversed(TI_Prices_list):

                        i += 1

                        if tp == '':
                            continue
                        #tpk = int(TI_Slots)-i
                        tpk = i
                        #print tpk,tp

                        if i_TI_Slots_Busy >= tpk:
                            continue

                        fti = round(float(tp),3)
            
                        if Clip_Budget_Start < fti:
                            continue

                        cur_Ow_Ds_Total_Paid =  data['Us_Md_Ow_Ds_Ti'][umi_key]['Media_Paid'] + fti
                        #data['Us_Md_Ow_Ds_Ti'][umi_key]['Media_Paid']
                        if cur_Ow_Ds_Total_Paid > f_Media_Cost:

                            flag_break = 1
                            print "***** !! flag_break = ",flag_break
                            print ID_Owner,Ds_key,ID_Time_Interval,\
                                "Media_Paid = ",f_Media_Cost,'/',data['Us_Md_Ow_Ds_Ti'][umi_key]['Media_Paid']
                            break

                        if (data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Total_Paid'][ID_Owner] + fti) >  \
                            Us_Md_Ow_Sum:

                            flag_break_Ow = 1
                            print "***** !! flag_break_Ow = ",flag_break_Ow
                            break


                        if (data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Paid'][ID_Owner][Ds_key] + fti) >  \
                            Us_Md_Ow_Ds_Sum:

                            flag_break_Ds = 1
                            print "***** !! flag_break_Ds = ",flag_break_Ds
                            break

                        i_TI_Slots_Busy += 1

                        if (Media_Cost_Ow_Ds_Ti - Paid) <= Clip_Budget_End:
                            #flag_break = 1
                            break

                        if (fti + Paid) > Media_Cost_Ow_Ds_Ti:
                            #flag_break = 1
                            break

                        if  Media_Cost_Ow_Ds_Ti - (fti + Paid) < 0:
                            #flag_break = 1
                            break



                        tMedia_Cost -=  fti
                        Paid   += fti

                        #print '====>',ID_Owner,Ds_key,ID_Time_Interval,fti,"Paid = ",Media_Cost_Ow_Ds_Ti,'/',Paid

                        #print '====>',ID_Owner,Ds_key,ID_Time_Interval,fti,"Paid = ",Paid,\
                        #    f_Media_Cost,'/',data['Us_Md_Ow_Ds_Ti'][umi_key]['Media_Paid'],\
                        #    data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Total_Paid'][ID_Owner],\
                        #    data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Paid'][ID_Owner][Ds_key],\
                        #    data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Paid'][ID_Owner][Ds_key][ID_Time_Interval]



                        data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Paid_Dict'][ID_Owner][Ds_key][ID_Time_Interval][tpk] = fti
                        data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Paid'][ID_Owner][Ds_key][ID_Time_Interval] += fti
                        data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Paid'][ID_Owner][Ds_key] += fti
                        data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Total_Paid'][ID_Owner] += fti
                        data['Us_Md_Ow_Ds_Ti'][umi_key]['Media_Paid'] += fti
        
                        if Clip_Budget_End >= tMedia_Cost:
                            #flag_break = 1
                            break
                        
                        Update_TI_Slots_Busy(\
                            data,\
                            i_TI_Slots_Busy,\
                            ID_Country ,\
                            ID_City  ,\
                            ID_Neighborhoods ,\
                            ID_Digital_Signage ,\
                            ID_Time_Interval )

                        DsTiNnUsMd_Key = Create_DsTiNnUsMd_Key(\
                            str(tpk)           ,\
                            ID_User           ,\
                            ID_User_Media)                   

                    if nTi < len_Us_Md_Ow_Ds_Ti_Sum_keys-1:
                        Delta_Ti += (Media_Cost_Ow_Ds_Ti - Paid)
                    else:
                        Delta_Ti = (Us_Md_Ow_Ds_Sum - Paid)


                    print ID_Owner,Ds_key,ID_Time_Interval,"Ow_Ds_Ti_Paid = ",Media_Cost_Ow_Ds_Ti,'/',data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Paid'][ID_Owner][Ds_key][ID_Time_Interval]
                    print ID_Owner,Ds_key,ID_Time_Interval,"Ow_Ds_Paid = ",Us_Md_Ow_Ds_Sum,'/',data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Paid'][ID_Owner][Ds_key]
                    print ID_Owner,Ds_key,ID_Time_Interval,"Ow_Ds_Total_Paid = ",Us_Md_Ow_Sum,'/',data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Total_Paid'][ID_Owner]
                    print ID_Owner,Ds_key,ID_Time_Interval,"Media_Paid = ",f_Media_Cost,'/',data['Us_Md_Ow_Ds_Ti'][umi_key]['Media_Paid']
                    print ID_Owner,Ds_key,ID_Time_Interval,"i_TI_Slots_Busy = ",TI_Slots,'/',i_TI_Slots_Busy
                    print ID_Owner,Ds_key,ID_Time_Interval,nTi,"Delta_Ti = ",Delta_Ti


                    if DsTiNnUsMd_Key != '':
                        data['Dig_Sign_Owner_TiNnUsMd'][Ow_Ds_key][ID_Time_Interval].append(DsTiNnUsMd_Key)  

                    if flag_break == 1:  break
                    if flag_break_Ow == 1:  break
                    if flag_break_Ds == 1:  break

                Delta_Ds = Delta_Ti
                print ID_Owner,Ds_key,ID_Time_Interval,nTi,"Delta_Ds = ",Delta_Ds


                if flag_break == 1:  break

                if flag_break_Ow == 1:  break

            Delta_Ow = Delta_Ds
            print ID_Owner,Ds_key,"Delta_Ow = ",Delta_Ow
            if flag_break == 1:  break


        print n,"END umi_key = ",umi_key
        #-------------------------------------------
        #if n >= 1:
        #    break   



