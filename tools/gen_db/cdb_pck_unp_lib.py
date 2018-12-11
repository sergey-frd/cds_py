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

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def Unpack_Ds_Val(Ds_Val):


    Dig_Sign_List   = Ds_Val.split(',')

    Dig_Sign        =     Dig_Sign_List[0]
    DS_Cost         = int(Dig_Sign_List[1])
    DS_Perc_Quality = int(Dig_Sign_List[2])

    return \
        Dig_Sign       ,      \
        DS_Cost        ,      \
        DS_Perc_Quality


#-------------------------------------------------------------------------------
def Unpack_User_Neighb_Ds_Md_Key(undm_key):

    undm_list          = undm_key.split(',')

    ID_User            = undm_list[0]
    ID_User_Media      = undm_list[1]
    ID_Country         = undm_list[2]
    ID_City            = undm_list[3]
    ID_Neighborhoods   = undm_list[4]
    ID_Digital_Signage = undm_list[5]
    ID_Owner           = undm_list[6]

    return \
        ID_User           ,      \
        ID_User_Media     ,      \
        ID_Country        ,      \
        ID_City           ,      \
        ID_Neighborhoods  ,      \
        ID_Digital_Signage,      \
        ID_Owner

#-------------------------------------------------------------------------------
def Unpack_User_Md_Val(umi_val):

    umi_val_list  = umi_val.split(',')

    ID_User_Media = umi_val_list[0]
    Media_Name    = umi_val_list[1]
    Media_Cost    = umi_val_list[2]
    Media_Slots   = umi_val_list[3]

    return  ID_User_Media,\
            Media_Name,      \
            Media_Cost,      \
            Media_Slots 

#-------------------------------------------------------------------------------
def Unpack_User_Md_Key(umi_key):

    umi_key_list   = umi_key.split(',')

    ID_User        = umi_key_list[0]
    ID_User_Media  = umi_key_list[1]

    return ID_User,      \
           ID_User_Media  

#-------------------------------------------------------------------------------
def Unpack_Udl_List(udl):

    udl_list = udl.split(',')
    tpk                     = udl_list[0]
    ID_Time_Interval        = udl_list[1]
    DS_TI_Price             = udl_list[2]
    TI_D_Sign_People        = udl_list[3]
    Dig_Sign                = udl_list[4]
    Owner_Name              = udl_list[5]
    ID_User                 = udl_list[6]
    ID_User_Media           = udl_list[7]
    ID_Country              = udl_list[8]
    ID_City                 = udl_list[9]
    ID_Neighborhoods        = udl_list[10]
    ID_Digital_Signage      = udl_list[11]
    ID_Owner                = udl_list[12]

    return \
        tpk               ,\
        ID_Time_Interval  ,\
        DS_TI_Price       ,\
        TI_D_Sign_People  ,\
        Dig_Sign          ,\
        Owner_Name        ,\
        ID_User           ,\
        ID_User_Media     ,\
        ID_Country        ,\
        ID_City           ,\
        ID_Neighborhoods  ,\
        ID_Digital_Signage,\
        ID_Owner

#-------------------------------------------------------------------------------
def Unpack_User_Nb__Ds_Md_List(undm_val):

    UsNeigDsMd_vl_list = undm_val.split(',')

    ID_User              = UsNeigDsMd_vl_list[0]
    ID_User_Media        = UsNeigDsMd_vl_list[1]
    ID_Country           = UsNeigDsMd_vl_list[2]
    ID_City              = UsNeigDsMd_vl_list[3]
    ID_Neighborhoods     = UsNeigDsMd_vl_list[4]
    ID_Digital_Signage   = UsNeigDsMd_vl_list[5]
    ID_Owner             = UsNeigDsMd_vl_list[6]
    Neighborhood         = UsNeigDsMd_vl_list[7]
    Nic_User             = UsNeigDsMd_vl_list[8]
    Dig_Sign             = UsNeigDsMd_vl_list[9]
    Owner_Name           = UsNeigDsMd_vl_list[10]
    Media_Name           = UsNeigDsMd_vl_list[11]
    Media_Cost           = UsNeigDsMd_vl_list[12]
    Media_Slots          = UsNeigDsMd_vl_list[13]
    Media_Total_Slots    = UsNeigDsMd_vl_list[14]
    DS_Cost              = UsNeigDsMd_vl_list[15]
    DS_Perc_Quality      = UsNeigDsMd_vl_list[16]
    UM_DS_COST           = UsNeigDsMd_vl_list[17]
    DS_Cost_Perc         = UsNeigDsMd_vl_list[18]
    DS_Media_Cost        = UsNeigDsMd_vl_list[19]
    DS_Media_Total_Slots = UsNeigDsMd_vl_list[20]


    return \
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
        DS_Media_Total_Slots 


#-----------------------------------------------------------
#----------------------------------------------------------
def Unpack_Ds_key(Ds_key):

    ds_list = Ds_key.split(',')

    ID_Country           = ds_list[0]
    ID_City              = ds_list[1]
    ID_Neighborhoods     = ds_list[2]
    ID_Digital_Signage   = ds_list[3]

    return \
        ID_Country           ,\
        ID_City              ,\
        ID_Neighborhoods     ,\
        ID_Digital_Signage 

#-----------------------------------------------------------
def Create_Ds_key(\
    ID_Country,
    ID_City,
    ID_Neighborhoods,
    ID_Digital_Signage):

    Ds_key = \
        ID_Country         +','+\
        ID_City            +','+\
        ID_Neighborhoods   +','+\
        ID_Digital_Signage

    return Ds_key
#-----------------------------------------------------------
def Create_Ow_Ds_key(\
    ID_Owner,
    ID_Country,
    ID_City,
    ID_Neighborhoods,
    ID_Digital_Signage):

    Ow_Ds_key = \
        ID_Owner           +','+\
        ID_Country         +','+\
        ID_City            +','+\
        ID_Neighborhoods   +','+\
        ID_Digital_Signage

    return Ow_Ds_key

#-------------------------------------------------------------------------------
def Create_Usdm_Key(\
    ID_User      ,
    ID_User_Media,
    ID_Country,
    ID_City,
    ID_Neighborhoods,
    ID_Digital_Signage,
    ID_Owner):

    usdm_key = \
        ID_User            +','+\
        ID_User_Media      +','+\
        ID_Country         +','+\
        ID_City            +','+\
        ID_Neighborhoods   +','+\
        ID_Digital_Signage +','+\
        ID_Owner 

    return usdm_key

#-------------------------------------------------------------------------------
def Create_Usdmt_Key(\
    ID_Country,
    ID_City,
    ID_Neighborhoods,
    ID_Digital_Signage,
    ID_Time_Interval):

    usdmt_key = \
        ID_Country         +','+\
        ID_City            +','+\
        ID_Neighborhoods   +','+\
        ID_Digital_Signage +','+\
        ID_Time_Interval 


    return usdmt_key

#-------------------------------------------------------------------------------
def Create_Umip_Val(\
    tpk                 ,
    ID_Time_Interval    ,
    DS_TI_Price         ,
    TI_D_Sign_People    ,
    Dig_Sign            ,
    Owner_Name          ,
    ID_User             ,   
    ID_User_Media       ,   
    ID_Country          ,   
    ID_City             ,   
    ID_Neighborhoods    ,   
    ID_Digital_Signage  ,   
    ID_Owner            ):

    umip_val = \
        tpk                 +','+\
        ID_Time_Interval    +','+\
        DS_TI_Price         +','+\
        TI_D_Sign_People    +','+\
        Dig_Sign            +','+\
        Owner_Name          +','+\
        ID_User             +','+\
        ID_User_Media       +','+\
        ID_Country          +','+\
        ID_City             +','+\
        ID_Neighborhoods    +','+\
        ID_Digital_Signage  +','+\
        ID_Owner          

    return umip_val

#-------------------------------------------------------------------------------
def Create_Neighb_Ds_Ti_Val(\
    ID_Country        ,
    ID_City           ,
    ID_Neighborhoods  ,
    ID_Digital_Signage,
    ID_Owner          ,
    ID_Time_Interval  ,
    Neighborhood      ,
    Dig_Sign          ,
    Owner_Name        ,
    DS_Cost           ,
    DS_Perc_Quality   ,
    TI_Price          ,
    TI_D_Sign_People  ,
    DS_TI_Price       ,
    TI_Slots          ,
    TI_Slots_Busy     ,
    TI_Slots_Free     ,
    TI_List_Prices):

    usdmt_val = \
        ID_Country         +','+\
        ID_City            +','+\
        ID_Neighborhoods   +','+\
        ID_Digital_Signage +','+\
        ID_Owner           +','+\
        ID_Time_Interval   +','+\
        Neighborhood       +','+\
        Dig_Sign           +','+\
        Owner_Name         +','+\
        DS_Cost            +','+\
        DS_Perc_Quality    +','+\
        TI_Price           +','+\
        TI_D_Sign_People   +','+\
        DS_TI_Price        +','+\
        TI_Slots           +','+\
        TI_Slots_Busy      +','+\
        TI_Slots_Free      +','+\
        TI_List_Prices

    return usdmt_val

#-------------------------------------------------------------------------------
def Unpack_Neighb_Ds_Ti_Key(usdmt_val):

    usdmt_val_list = usdmt_val.split(',')

    ID_Country            = usdmt_val_list[0]
    ID_City               = usdmt_val_list[1]
    ID_Neighborhoods      = usdmt_val_list[2]
    ID_Digital_Signage    = usdmt_val_list[3]
    ID_Owner              = usdmt_val_list[4]
    ID_Time_Interval      = usdmt_val_list[5]
    Neighborhood          = usdmt_val_list[6]
    Dig_Sign              = usdmt_val_list[7]
    Owner_Name            = usdmt_val_list[8]
    DS_Cost               = usdmt_val_list[9]
    DS_Perc_Quality       = usdmt_val_list[10]
    TI_Price              = usdmt_val_list[11]
    TI_D_Sign_People      = usdmt_val_list[12] 
    DS_TI_Price           = usdmt_val_list[13]
    TI_Slots              = usdmt_val_list[14]
    TI_Slots_Busy         = usdmt_val_list[15]
    TI_Slots_Free         = usdmt_val_list[16]
    TI_List_Prices        = usdmt_val_list[17]  

    return \
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
        TI_List_Prices

#-------------------------------------------------------------------------------

def Update_TI_Slots_Busy(\
    data,\
    i_TI_Slots_Busy,\
    ID_Country ,\
    ID_City  ,\
    ID_Neighborhoods ,\
    ID_Digital_Signage ,\
    ID_Time_Interval ):


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

    usdmt_val = Create_Neighb_Ds_Ti_Val(\
        ID_Country          ,
        ID_City             ,
        ID_Neighborhoods    ,
        ID_Digital_Signage  ,
        ID_Owner            ,
        ID_Time_Interval    ,
        Neighborhood        ,
        Dig_Sign            ,
        Owner_Name          ,
        DS_Cost             ,
        DS_Perc_Quality     ,
        TI_Price            ,
        TI_D_Sign_People    ,
        DS_TI_Price         ,
        TI_Slots            ,
        str(i_TI_Slots_Busy),
        TI_Slots_Free       ,
        TI_List_Prices      )   


#-------------------------------------------------------------------------------
def Create_DsTiNnUsMd_Key(\
    TI_Slot      ,
    ID_User      ,
    ID_User_Media):

    DsTiNnUsMd_Key = \
        TI_Slot            +','+\
        ID_User            +','+\
        ID_User_Media 

    return DsTiNnUsMd_Key

