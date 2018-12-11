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
#-------------------------------------------------------------------------------

def Optim_Plan(data, con, cur): 

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
    #def random_opt(domain, costf):
    def random_opt(data_opt):

     costf = dorm_cost_
     best=999999999
     bestr=None

     for i in xrange(0, 1000):
      # Выбрать случаиное решение


      domain = data_opt['user'].keys()
      #domain = data_opt['user_key_list']

      #domain = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
      #w_domain = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
      w_domain = domain
      #print 'w_domain=',w_domain
      
      #------------------------------------
      r = list()
      for j in xrange(len(domain)):
          x = random.choice(w_domain)
          #x = random.randint(0, w_domain[j])
          r.append(x)
          #print j,'x->',x,'w_domain->', w_domain,'r==>', r
          w_domain.remove(x)

      # Get the cost
      cost = costf(r,data_opt)

      # Сравнить со стоимостью наилучшего наиденного к этому моменту решения
      if cost < best:
       best = cost
       bestr = r
       print '-->bestr=',bestr,cost

     return bestr, best

    #-------------------------------------------------------------------------------
    #    Целевая функция работает следующим 
    #    образом.  Создается начальный список 
    #    отсеков, и уже использованные отсеки из 
    #    него удаляются.  Стоимость вычисляется 
    #    путем сравнения комнаты, в которую 
    #    студент помещен, с двумя его 
    #    пожеланиями.  Стоимость не изменяется, 
    #    если студенту досталась та комната, в 
    #    которую он больше всего хотел 
    #    поселиться; увеличивается на 1, если это 
    #    второе из его пожеланий; и увеличивается 
    #    на 3, если он вообще не хотел жить в этой 
    #    комнате.

    def dorm_cost_(vec,data_opt):

        #print '-->vec=',vec
        cost=0

        # Создаем список отсеков, т.е. первые 2 места - 0 отсек и т.д.
        #slots = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
        slots = data_opt['rms_slots']

        #slots = list()  
        #rms_keys = data_opt['rms'].keys()
        #for rms_key in rms_keys:
        #    for i in xrange(0,slot_count):
        #        slots.append(int(rms_key))

        #print '-->slots=',slots

        # Цикл по студентам, i - порядковый номер студента
        for i in xrange(len(vec)):
            x = int(vec[i])
            #print 'x->',x
            #print 'slots[x]->',slots[x]

            #dorm = dorms[slots[x]]
            dorm = data_opt['dorms'] [slots[x]]

            pref = prefs[i][1]
            #pref = data_opt['user_pref'][str(x)] 
            #print i,x, '->', slots[x],'->', prefs[i][0], pref, '->', dorm

            # Стоимость основного пожелания равна 0, альтернативного – 1
            # Если комната не входит в список пожеланий, стоимость увеличивается на 3

            if pref[0] == dorm: cost += 0
            #if pref['0'] == dorm: cost += 0
            elif pref[1] == dorm: cost += 1
            #elif pref['1'] == dorm: cost += 1
            else: cost += 3

        #print '*=>cost=',cost
        return cost

    #-------------------------------------------------------------------------------
    print '***************************************'
    print '***************************************'



    data_opt = dict() 
     
    data_opt['base'] = dict()  

    data_opt['slot_count'] = 2

    data_opt['rms'] = dict()  
    data_opt['rms']['0'] = 'Zeus'    
    data_opt['rms']['1'] = 'Athena'   
    data_opt['rms']['2'] = 'Hercules'   
    data_opt['rms']['3'] = 'Bacchus'   
    data_opt['rms']['4'] = 'Pluto'   

    data_opt['user'] = dict()  
    data_opt['user']['0'] = 'Toby'    
    data_opt['user']['1'] = 'Steve'   
    data_opt['user']['2'] = 'Karen'   
    data_opt['user']['3'] = 'Sarah'   
    data_opt['user']['4'] = 'Dave'    
    data_opt['user']['5'] = 'Jeff'    
    data_opt['user']['6'] = 'Fred'    
    data_opt['user']['7'] = 'Suzie'   
    data_opt['user']['8'] = 'Laura'   
    data_opt['user']['9'] = 'James' 
 
    data_opt['user_pref'] = dict()  
    data_opt['user_pref']['0']      = dict()     
    data_opt['user_pref']['0']['0'] = 'Bacchus'      
    data_opt['user_pref']['0']['1'] = 'Hercules'     
    data_opt['user_pref']['1']      = dict()     
    data_opt['user_pref']['1']['0'] = 'Zeus'      
    data_opt['user_pref']['1']['1'] = 'Pluto'     
    data_opt['user_pref']['2']      = dict()     
    data_opt['user_pref']['2']['0'] = 'Athena'     
    data_opt['user_pref']['2']['1'] = 'Zeus'       
    data_opt['user_pref']['3']      = dict()     
    data_opt['user_pref']['3']['0'] = 'Zeus'       
    data_opt['user_pref']['3']['1'] = 'Pluto'      
    data_opt['user_pref']['4']      = dict()     
    data_opt['user_pref']['4']['0'] = 'Athena'      
    data_opt['user_pref']['4']['1'] = 'Bacchus'     
    data_opt['user_pref']['5']      = dict()     
    data_opt['user_pref']['5']['0'] = 'Hercules'    
    data_opt['user_pref']['5']['1'] = 'Pluto'       
    data_opt['user_pref']['6']      = dict()     
    data_opt['user_pref']['6']['0'] = 'Pluto'      
    data_opt['user_pref']['6']['1'] = 'Athena'     
    data_opt['user_pref']['7']      = dict()     
    data_opt['user_pref']['7']['0'] = 'Bacchus'     
    data_opt['user_pref']['7']['1'] = 'Hercules'    
    data_opt['user_pref']['8']      = dict()     
    data_opt['user_pref']['8']['0'] = 'Bacchus'      
    data_opt['user_pref']['8']['1'] = 'Hercules'     
    data_opt['user_pref']['9']      = dict()   
    data_opt['user_pref']['9']['0'] = 'Hercules'   
    data_opt['user_pref']['9']['1'] = 'Athena'     
 

    data_opt['user_prior'] = dict()  
    data_opt['user_prior']['0,0'] = 'Bacchus'   
    data_opt['user_prior']['0,1'] = 'Hercules'  
    data_opt['user_prior']['1,0'] = 'Zeus'     
    data_opt['user_prior']['1,1'] = 'Pluto'    
    data_opt['user_prior']['2,0'] = 'Athena'   
    data_opt['user_prior']['2,1'] = 'Zeus'     
    data_opt['user_prior']['3,0'] = 'Zeus'     
    data_opt['user_prior']['3,1'] = 'Pluto'    
    data_opt['user_prior']['4,0'] = 'Athena'    
    data_opt['user_prior']['4,1'] = 'Bacchus'   
    data_opt['user_prior']['5,0'] = 'Hercules'  
    data_opt['user_prior']['5,1'] = 'Pluto'     
    data_opt['user_prior']['6,0'] = 'Pluto'     
    data_opt['user_prior']['6,1'] = 'Athena'    
    data_opt['user_prior']['7,0'] = 'Bacchus'  
    data_opt['user_prior']['7,1'] = 'Hercules' 
    data_opt['user_prior']['8,0'] = 'Bacchus'  
    data_opt['user_prior']['8,1'] = 'Hercules' 
    data_opt['user_prior']['9,0'] = 'Hercules' 
    data_opt['user_prior']['9,1'] = 'Athena'   

    data_opt['slot'] = dict()  
    data_opt['slot']['0'] = 'slot_0'    
    data_opt['slot']['1'] = 'slot_1' 

    #data_opt['rms_slot_indx'] = dict()  
    #data_opt['rms_slot_indx']['0'] = '0,0,Zeus,slot_0'    
    #data_opt['rms_slot_indx']['1'] = '0,1,Zeus,slot_1'    
    #data_opt['rms_slot_indx']['2'] = '1,0,Athena,slot_0'   
    #data_opt['rms_slot_indx']['3'] = '1,1,Athena,slot_1'   
    #data_opt['rms_slot_indx']['4'] = '2,0,Hercules,slot_0'   
    #data_opt['rms_slot_indx']['5'] = '2,1,Hercules,slot_1'   
    #data_opt['rms_slot_indx']['6'] = '3,0,Bacchus,slot_0'   
    #data_opt['rms_slot_indx']['7'] = '3,1,Bacchus,slot_1'   
    #data_opt['rms_slot_indx']['8'] = '4,0,Pluto,slot_0'    
    #data_opt['rms_slot_indx']['9'] = '4,1,Pluto,slot_1'    

    data_opt['rms_slot_indx'] = dict()  
    data_opt['rms_slot_indx']['0'] = '0,0'
    data_opt['rms_slot_indx']['1'] = '0,1'
    data_opt['rms_slot_indx']['2'] = '1,0'
    data_opt['rms_slot_indx']['3'] = '1,1'
    data_opt['rms_slot_indx']['4'] = '2,0' 
    data_opt['rms_slot_indx']['5'] = '2,1' 
    data_opt['rms_slot_indx']['6'] = '3,0'
    data_opt['rms_slot_indx']['7'] = '3,1'
    data_opt['rms_slot_indx']['8'] = '4,0'
    data_opt['rms_slot_indx']['9'] = '4,1'

    data_opt['rms_slot_dict'] = dict()  
    data_opt['rms_slot_dict']['0,0'] = '0'
    data_opt['rms_slot_dict']['0,1'] = '1'
    data_opt['rms_slot_dict']['1,0'] = '2'
    data_opt['rms_slot_dict']['1,1'] = '3'
    data_opt['rms_slot_dict']['2,0'] = '4'
    data_opt['rms_slot_dict']['2,1'] = '5'
    data_opt['rms_slot_dict']['3,0'] = '6'
    data_opt['rms_slot_dict']['3,1'] = '7'
    data_opt['rms_slot_dict']['4,0'] = '8'
    data_opt['rms_slot_dict']['4,1'] = '9'
    #-------------------------------------------

    data_opt['rms_slots'] = list()  
    data_opt['dorms'] = list()  
    slot_count = data_opt['slot_count']

    rms_keys = data_opt['rms'].keys()
    for rms_key in rms_keys:
        data_opt['dorms'].append(data_opt['rms'][rms_key])
        for i in xrange(0,slot_count):
            data_opt['rms_slots'].append(int(rms_key))


    #data_opt['user_key_list'] = list() 
    #user_keys = data_opt['user'].keys()  
    #for user_key in user_keys:
    #    data_opt['user_key_list'].append(user_key)


    #data_opt['user_key_list'] = list() 
    data_opt['user_key_list'] = data_opt['user'].keys()

    ##-------------------------------------------
    ## Двухместные комнаты
    dorms = ['Zeus','Athena','Hercules','Bacchus','Pluto']
    #dormss = ['0 Zeus','1 Athena','2 Hercules','3 Bacchus','4 Pluto']
    #
    ## Люди и два пожелания у каждого (основное, второстепенное)
    prefs = [('Toby', ('Bacchus', 'Hercules')),
        ('Steve', ('Zeus', 'Pluto')),
        ('Karen', ('Athena', 'Zeus')),
        ('Sarah', ('Zeus', 'Pluto')),
        ('Dave', ('Athena', 'Bacchus')), 
        ('Jeff', ('Hercules', 'Pluto')), 
        ('Fred', ('Pluto', 'Athena')), 
        ('Suzie', ('Bacchus', 'Hercules')), 
        ('Laura', ('Bacchus', 'Hercules')), 
        ('James', ('Hercules', 'Athena'))]
    
    ##  список отсеков, т.е. первые 2 места - 0 отсек и т.д.
    slots = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
    #slotss = ['0 0 Zeus', '1 0 Zeus', '2 1 Athena', '3 1 Athena', '4 2 Hercules', '5 2 Hercules', '6 3 Bacchus', '7 3 Bacchus', '8 4 Pluto', '9 4 Pluto']
    #
    ## [9, 8, 7, 6,..., 1]
    ##domain = [i for i in xrange(9, 0, -1)]
    #
    ##domain = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ##print 'domain=',domain
    #
    #print 'prefs='
    #pprint (prefs)
    #
    #print 'dorms=',dorms
    #print 'dormss=',dormss
    #
    #print 'slots='
    #pprint (slots)
    #
    #print 'slotss=',slotss

    #i = 0
    #for pr in prefs:
    #    print i,pr[i]
    #    i += 1

    print '***************************************'
    result, score = random_opt(data_opt)
    print 'random_optimize dorm_cost result=',result, 'score=',score

    print '***************************************'
    i = 0
    for x in result:
        dorm = dorms[slots[int(x)]]
        pref = prefs[i][1]

        rms_slot_indx_val = data_opt['rms_slot_indx'][str(x)]
        rms_slot_indx_list = rms_slot_indx_val.split(',')
        rms_key  = rms_slot_indx_list[0]
        slot_key = rms_slot_indx_list[1]

        rms  = data_opt['rms'][rms_key]
        slot = data_opt['slot'][slot_key]

        #print i,int(x), '->', slots[int(x)],'->', prefs[i][0], pref, '->', dorm
        #print 'i=',i,'stud ->', prefs[i][0],\
        #    '-> pref ->', pref , \
        #    '; x=', int(x), \
        #    'slots[x]=',slots[int(x)],\
        #    '-> room ->', dorm,\
        #    data_opt['rms_slot_indx'][str(x)] 


        print 'user i=', i,'=>', data_opt['user'][str(i)] ,';',\
          data_opt['user_prior'][str(i)+','+str(0)], \
          data_opt['user_prior'][str(i)+','+str(1)], \
          '; x=', int(x), \
           data_opt['rms'][rms_key],\
           data_opt['slot'][slot_key]



        #print 'x=',x
        #print 'rms_slot_indx=',data_opt['rms_slot_indx'][str(x)]

          #,\
          #data_opt['rms_slot_indx'][x] 
        i += 1

    print "---------------"

    #print 'data_opt='
    #pprint (data_opt)

    #print 'data_opt[rms_slot_indx]='
    #pprint (data_opt['rms_slot_indx'])
    #
    #
    #print 'data_opt[rms_slot_indx][5]='
    #pprint (data_opt['rms_slot_indx']['5'])
