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
#-------------------------------------------------------------------------------

##from lib_py_utils        import *
###from scan_utils         import *
## from scan_utils2         import *

from difflib             import *
from pprint              import *


##from main_doxy4ug_lib_j import *
## from ug_api_cases       import *

import random
from random import randint
import math


#-------------------------------------------------------------------------------
# pop_size - размер популяции
# mutprob - чем меньше, тем реже берем мутацию и чаще скрещивание
# elite - Доля особеq в популяции, считающихся хорошими решениями и переходящих в следующее поколение
# maxiter - Количество поколений
def genetic_optimize(domain, costf, pop_size=50, step=1, mutprob=0.2, elite=0.2, maxiter=100):
 
 # Мутация
 def mutate(vec):
  i = random.randint(0, len(domain)-1)
  if vec[i] < domain[i]:
   return vec[0:i]+[vec[i]+step]+vec[i+1:]
  else:
   return vec[0:i]+[vec[i]-step]+vec[i+1:]

 # Скрещивание
 def crossover(r1, r2):
  i = random.randint(1, len(domain)-2)
  return r1[0:i]+r2[i:]

 # Создаем первую популяцию
 pop = []
 for i in xrange(pop_size):
  vec = [random.randint(0, domain[i]) for i in xrange(len(domain))]
  pop.append(vec)

 # Сколько лучших оставляем из каждого поколения
 topelite = int(elite*pop_size)

 for i in xrange(maxiter):
  scores = [(costf(v), v) for v in pop]
  scores.sort()
  ranked = [v for (s,v) in scores]

  # Сначала включаем только победителеи
  pop = ranked[0:topelite]

  # Добавляем особей, полученных мутацией и скрещиванием победивших родителей
  while len(pop) < pop_size:

   if random.random() < mutprob:
    # Мутация
    c = random.randint(0, topelite)
    pop.append(mutate(ranked[c]))

   else:
    # Скрещивание
    c1 = random.randint(0, topelite)
    c2 = random.randint(0, topelite)
    pop.append(crossover(ranked[c1], ranked[c2]))

 return scores[0][1], scores[0][0]
#-------------------------------------------------------------------------------

def annealing_optimize(domain, costf, T=10000.0, cool=0.99, step=1):
 
 # Выбрать случаиное решение
 vec = [random.randint(0, domain[i]) for i in xrange(len(domain))]

 while T > 0.1:
  # Выбрать один из индексов
  i = random.randint(0, len(domain)-1)

  # Выбрать направление изменения
  dir = random.randint(-step, step)

  # Создать новыи список, в котором одно значение изменено
  vecb = vec[:]
  vecb[i] += dir
  if vecb[i] < 0: vecb[i] = 0
  elif vecb[i] > domain[i]: vecb[i] = domain[i]

  # Вычислить текущую и новую стоимость
  ea = costf(vec)
  eb = costf(vecb)
  p = pow(math.e, (-eb-ea)/T)

  # Новое решение лучше? Если нет, метнем кости
  if (eb < ea or random.random() < p):
   vec = vecb      

  # Уменьшить температуру
  T = T * cool
 return vec, eb


#-------------------------------------------------------------------------------
def hill_climb(domain, costf):

 # Выбрать случаиное решение
 sol = [random.randint(0, domain[i]) for i in xrange(len(domain))]
 best = costf(sol)

 # Главныи цикл
 is_stop = False
 while not is_stop:
  # Создать список соседних решении
  neighbors = []
  for j in xrange(len(domain)):

   # Отходим на один шаг в каждом направлении
   if 0 < sol[j] < 9:
    neighbors.append(sol[0:j] + [sol[j]+1] + sol[j+1:])
    neighbors.append(sol[0:j] + [sol[j]-1] + sol[j+1:])

   if 0 == sol[j]:
    neighbors.append(sol[0:j] + [sol[j]+1] + sol[j+1:])

   if sol[j] == domain[j]:
    neighbors.append(sol[0:j] + [sol[j]-1] + sol[j+1:])

  # Ищем наилучшее из соседних решении

  is_stop = True
  for j in xrange(len(neighbors)):
   cost = costf(neighbors[j])
   if cost < best:
    is_stop = False
    best = cost
    sol = neighbors[j]

 return sol, best


#-------------------------------------------------------------------------------
def random_optimize(domain, costf):
 best=999999999
 bestr=None

 for i in xrange(0, 2):
  # Выбрать случаиное решение
  r = [random.randint(0, domain[i]) for i in xrange(len(domain))]

  # Get the cost
  cost = costf(r)

  # Сравнить со стоимостью наилучшего наиденного к этому моменту решения
  if cost < best:
   best = cost
   bestr = r
   print '-->bestr=',bestr

 return bestr, best
#-------------------------------------------------------------------------------
def get_minutes(t):
    x=time.strptime(t,'%H:%M')
    return x[3]*60+x[4]
#-------------------------------------------------------------------------------
def schedule_cost(sol):
    totalprice = 0
    latestarrival = 0
    earliestdep = 24*60



    peoples = [('Seymour','BOS'),
        ('Franny','DAL'),
        ('Zooey','CAK'),
        ('Walt','MIA'),
        ('Buddy','ORD'),
        ('Les','OMA')]

    flights = {('LGA', 'CAK'): [('6:58', '9:01', 238), ('8:19', '11:16', 122), ('9:58', '12:56', 249), ('10:32', '13:16', 139), ('12:01', '13:41', 267), ('13:37', '15:33', 142), ('15:50', '18:45', 243), ('16:33', '18:15', 253), ('18:17', '21:04', 259), ('19:46', '21:45', 214)], ('DAL', 'LGA'): [('6:12', '10:22', 230), ('7:53', '11:37', 433), ('9:08', '12:12', 364), ('10:30', '14:57', 290), ('12:19', '15:25', 342), ('13:54', '18:02', 294), ('15:44', '18:55', 382), ('16:52', '20:48', 448), ('18:26', '21:29', 464), ('20:07', '23:27', 473)], ('LGA', 'BOS'): [('6:39', '8:09', 86), ('8:23', '10:28', 149), ('9:58', '11:18', 130), ('10:33', '12:03', 74), ('12:08', '14:05', 142), ('13:39', '15:30', 74), ('15:25', '16:58', 62), ('17:03', '18:03', 103), ('18:24', '20:49', 124), ('19:58', '21:23', 142)], ('LGA', 'MIA'): [('6:33', '9:14', 172), ('8:23', '11:07', 143), ('9:25', '12:46', 295), ('11:08', '14:38', 262), ('12:37', '15:05', 170), ('14:08', '16:09', 232), ('15:23', '18:49', 150), ('16:50', '19:26', 304), ('18:07', '21:30', 355), ('20:27', '23:42', 169)], ('LGA', 'OMA'): [('6:19', '8:13', 239), ('8:04', '10:59', 136), ('9:31', '11:43', 210), ('11:07', '13:24', 171), ('12:31', '14:02', 234), ('14:05', '15:47', 226), ('15:07', '17:21', 129), ('16:35', '18:56', 144), ('18:25', '20:34', 205), ('20:05', '21:44', 172)], ('OMA', 'LGA'): [('6:11', '8:31', 249), ('7:39', '10:24', 219), ('9:15', '12:03', 99), ('11:08', '13:07', 175), ('12:18', '14:56', 172), ('13:37', '15:08', 250), ('15:03', '16:42', 135), ('16:51', '19:09', 147), ('18:12', '20:17', 242), ('20:05', '22:06', 261)], ('CAK', 'LGA'): [('6:08', '8:06', 224), ('8:27', '10:45', 139), ('9:15', '12:14', 247), ('10:53', '13:36', 189), ('12:08', '14:59', 149), ('13:40', '15:38', 137), ('15:23', '17:25', 232), ('17:08', '19:08', 262), ('18:35', '20:28', 204), ('20:30', '23:11', 114)], ('LGA', 'DAL'): [('6:09', '9:49', 414), ('7:57', '11:15', 347), ('9:49', '13:51', 229), ('10:51', '14:16', 256), ('12:20', '16:34', 500), ('14:20', '17:32', 332), ('15:49', '20:10', 497), ('17:14', '20:59', 277), ('18:44', '22:42', 351), ('19:57', '23:15', 512)], ('LGA', 'ORD'): [('6:03', '8:43', 219), ('7:50', '10:08', 164), ('9:11', '10:42', 172), ('10:33', '13:11', 132), ('12:08', '14:47', 231), ('14:19', '17:09', 190), ('15:04', '17:23', 189), ('17:06', '20:00', 95), ('18:33', '20:22', 143), ('19:32', '21:25', 160)], ('ORD', 'LGA'): [('6:05', '8:32', 174), ('8:25', '10:34', 157), ('9:42', '11:32', 169), ('11:01', '12:39', 260), ('12:44', '14:17', 134), ('14:22', '16:32', 126), ('15:58', '18:40', 173), ('16:43', '19:00', 246), ('18:48', '21:45', 246), ('19:50', '22:24', 269)], ('MIA', 'LGA'): [('6:25', '9:30', 335), ('7:34', '9:40', 324), ('9:15', '12:29', 225), ('11:28', '14:40', 248), ('12:05', '15:30', 330), ('14:01', '17:24', 338), ('15:34', '18:11', 326), ('17:07', '20:04', 291), ('18:23', '21:35', 134), ('19:53', '22:21', 173)], ('BOS', 'LGA'): [('6:17', '8:26', 89), ('8:04', '10:11', 95), ('9:45', '11:50', 172), ('11:16', '13:29', 83), ('12:34', '15:02', 109), ('13:40', '15:37', 138), ('15:27', '17:18', 151), ('17:11', '18:30', 108), ('18:34', '19:36', 136), ('20:17', '22:22', 102)]}


    destination = 'LGA'

    #sol = list()
    #print 'sol=',sol
    
    
    for d in xrange(len(sol)/2):
        origin = peoples[d][1]
        outbound = flights[(origin, destination)][int(sol[d])]
        returnf = flights[(destination, origin)][int(sol[d+1])]
    
        totalprice += outbound[2]
        totalprice += returnf[2]
    
        if latestarrival < get_minutes(outbound[1]): latestarrival = get_minutes(outbound[1])
        if earliestdep > get_minutes(returnf[0]): earliestdep = get_minutes(returnf[0])
    
    totalwait = 0  
    
    for d in xrange(len(sol)/2):
        origin = peoples[d][1]
        outbound = flights[(origin, destination)][int(sol[d])]
        returnf = flights[(destination, origin)][int(sol[d+1])]
        totalwait += latestarrival - get_minutes(outbound[1])
        totalwait += get_minutes(returnf[0]) - earliestdep  
    
    #print 'totalprice=',totalprice
    if latestarrival > earliestdep: totalprice += 50
    
    return totalprice + totalwait
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

    #-------------------------------------------------------------------------------
    # pop_size - размер популяции
    # mutprob - чем меньше, тем реже берем мутацию и чаще скрещивание
    # elite - Доля особеq в популяции, считающихся хорошими решениями и переходящих в следующее поколение
    # maxiter - Количество поколений
    def genetic_opt(domain, costf, pop_size=50, step=1, mutprob=0.2, elite=0.2, maxiter=100):
     

     w_domain = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

     # Мутация
     def mutate(vec):
      i = random.randint(0, len(domain)-1)
      if vec[i] < domain[i]:
       return vec[0:i]+[vec[i]+step]+vec[i+1:]
      else:
       return vec[0:i]+[vec[i]-step]+vec[i+1:]

     # Скрещивание
     def crossover(r1, r2):
      i = random.randint(1, len(domain)-2)
      return r1[0:i]+r2[i:]

     # Создаем первую популяцию
     pop = []
     for i in xrange(pop_size):
      vec = [random.randint(0, domain[i]) for i in xrange(len(domain))]

      ##------------------------------------
      #vec = list()
      #for j in xrange(len(domain)):
      #    x = random.choice(w_domain)
      #    vec.append(x)
      #    k = 0
      #    for ix in w_domain:
      #      if x == ix:
      #          del w_domain[k]
      #          break
      #      k += 1
      #  #------------------------------------
      pop.append(vec)

     # Сколько лучших оставляем из каждого поколения
     topelite = int(elite*pop_size)

     for i in xrange(maxiter):
      scores = [(costf(v), v) for v in pop]
      scores.sort()
      ranked = [v for (s,v) in scores]

      # Сначала включаем только победителеи
      pop = ranked[0:topelite]

      # Добавляем особей, полученных мутацией и скрещиванием победивших родителей
      while len(pop) < pop_size:

       if random.random() < mutprob:
        # Мутация
        c = random.randint(0, topelite)
        pop.append(mutate(ranked[c]))

       else:
        # Скрещивание
        c1 = random.randint(0, topelite)
        c2 = random.randint(0, topelite)
        pop.append(crossover(ranked[c1], ranked[c2]))

     return scores[0][1], scores[0][0]


    #-------------------------------------------------------------------------------
    def random_opt(domain, costf):
     best=999999999
     bestr=None

     for i in xrange(0, 1000):
      # Выбрать случаиное решение
      r = [random.randint(0, domain[i]) for i in xrange(len(domain))]

      ##slots = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
      ##len_slots = len(slots)
      w_domain = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
      #print 'w_domain=',w_domain
      
      #------------------------------------
      r = list()
      for j in xrange(len(domain)):
          x = random.choice(w_domain)
          #x = random.randint(0, w_domain[j])
          r.append(x)

          #print j,'x->',x,'w_domain->', w_domain,'r==>', r
          k = 0
          for ix in w_domain:
            if x == ix:
                del w_domain[k]
                break
            k += 1
        #------------------------------------

      # Get the cost
      cost = costf(r)

      # Сравнить со стоимостью наилучшего наиденного к этому моменту решения
      if cost < best:
       best = cost
       bestr = r
       print '-->bestr=',bestr,cost

     return bestr, best

    #-------------------------------------------------------------------------------
    def dorm_cost_(vec):

     #print '-->vec=',vec
     cost=0

     # Создаем список отсеков, т.е. первые 2 места - 0 отсек и т.д.
     slots = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
     #print '-->slots=',slots

     # Цикл по студентам, i - порядковый номер студента
     for i in xrange(len(vec)):
      x = int(vec[i])
      #print 'x->',x
      #print 'slots[x]->',slots[x]
      dorm = dorms[slots[x]]
      pref = prefs[i][1]
      #print i,x, '->', slots[x],'->', prefs[i][0], pref, '->', dorm

      # Стоимость основного пожелания равна 0, альтернативного – 1
      # Если комната не входит в список пожеланий, стоимость увеличивается на 3

      #if pref[0] == dorm: cost += 0; print i,'+= 0 cost=',cost
      #elif pref[1] == dorm: cost += 1; print i,'+= 1 cost=',cost
      #else: cost += 3; print i,'+= 3 cost=',cost

      if pref[0] == dorm: cost += 0
      elif pref[1] == dorm: cost += 1
      else: cost += 3

      #print i,'cost=',cost
      # Удалить выбранный отсек
      # Это самое важное действие тут,
      # прошу особо обратить на него внимание и учесть, что элементы сдвигаются

      ###del slots[x]

      #k = 0
      #for ix in slots:
      #  if ix == slots[x]:
      #      del slots[k]
      #      print ix,'del slots[k] =',slots[k]
      #      break
      #  k += 1
      #
      #print i,x,'->slots=',slots

     #print '*=>cost=',cost
     return cost
    #-------------------------------------------------------------------------------
    def dorm_cost(vec):

     cost=0

     # Создаем список отсеков, т.е. первые 2 места - 0 отсек и т.д.
     slots = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]

     # Цикл по студентам, i - порядковый номер студента
     for i in xrange(len(vec)):
      x = int(vec[i])
      dorm = dorms[slots[x]]
      pref = prefs[i][1]
      #print x, '->', slots[x],'->', prefs[i][0], pref, '->', dorm

      # Стоимость основного пожелания равна 0, альтернативного – 1
      # Если комната не входит в список пожеланий, стоимость увеличивается на 3
      if pref[0] == dorm: cost += 0
      elif pref[1] == dorm: cost += 1
      else: cost += 3

      # Удалить выбранный отсек
      # Это самое важное действие тут,
      # прошу особо обратить на него внимание и учесть, что элементы сдвигаются
      del slots[x]

     return cost

     #-------------------------------------------------------------------------------



    peoples = [('Seymour','BOS'),
        ('Franny','DAL'),
        ('Zooey','CAK'),
        ('Walt','MIA'),
        ('Buddy','ORD'),
        ('Les','OMA')]

    destination = 'LGA'

    flights = {('LGA', 'CAK'): [('6:58', '9:01', 238), ('8:19', '11:16', 122), ('9:58', '12:56', 249), ('10:32', '13:16', 139), ('12:01', '13:41', 267), ('13:37', '15:33', 142), ('15:50', '18:45', 243), ('16:33', '18:15', 253), ('18:17', '21:04', 259), ('19:46', '21:45', 214)], ('DAL', 'LGA'): [('6:12', '10:22', 230), ('7:53', '11:37', 433), ('9:08', '12:12', 364), ('10:30', '14:57', 290), ('12:19', '15:25', 342), ('13:54', '18:02', 294), ('15:44', '18:55', 382), ('16:52', '20:48', 448), ('18:26', '21:29', 464), ('20:07', '23:27', 473)], ('LGA', 'BOS'): [('6:39', '8:09', 86), ('8:23', '10:28', 149), ('9:58', '11:18', 130), ('10:33', '12:03', 74), ('12:08', '14:05', 142), ('13:39', '15:30', 74), ('15:25', '16:58', 62), ('17:03', '18:03', 103), ('18:24', '20:49', 124), ('19:58', '21:23', 142)], ('LGA', 'MIA'): [('6:33', '9:14', 172), ('8:23', '11:07', 143), ('9:25', '12:46', 295), ('11:08', '14:38', 262), ('12:37', '15:05', 170), ('14:08', '16:09', 232), ('15:23', '18:49', 150), ('16:50', '19:26', 304), ('18:07', '21:30', 355), ('20:27', '23:42', 169)], ('LGA', 'OMA'): [('6:19', '8:13', 239), ('8:04', '10:59', 136), ('9:31', '11:43', 210), ('11:07', '13:24', 171), ('12:31', '14:02', 234), ('14:05', '15:47', 226), ('15:07', '17:21', 129), ('16:35', '18:56', 144), ('18:25', '20:34', 205), ('20:05', '21:44', 172)], ('OMA', 'LGA'): [('6:11', '8:31', 249), ('7:39', '10:24', 219), ('9:15', '12:03', 99), ('11:08', '13:07', 175), ('12:18', '14:56', 172), ('13:37', '15:08', 250), ('15:03', '16:42', 135), ('16:51', '19:09', 147), ('18:12', '20:17', 242), ('20:05', '22:06', 261)], ('CAK', 'LGA'): [('6:08', '8:06', 224), ('8:27', '10:45', 139), ('9:15', '12:14', 247), ('10:53', '13:36', 189), ('12:08', '14:59', 149), ('13:40', '15:38', 137), ('15:23', '17:25', 232), ('17:08', '19:08', 262), ('18:35', '20:28', 204), ('20:30', '23:11', 114)], ('LGA', 'DAL'): [('6:09', '9:49', 414), ('7:57', '11:15', 347), ('9:49', '13:51', 229), ('10:51', '14:16', 256), ('12:20', '16:34', 500), ('14:20', '17:32', 332), ('15:49', '20:10', 497), ('17:14', '20:59', 277), ('18:44', '22:42', 351), ('19:57', '23:15', 512)], ('LGA', 'ORD'): [('6:03', '8:43', 219), ('7:50', '10:08', 164), ('9:11', '10:42', 172), ('10:33', '13:11', 132), ('12:08', '14:47', 231), ('14:19', '17:09', 190), ('15:04', '17:23', 189), ('17:06', '20:00', 95), ('18:33', '20:22', 143), ('19:32', '21:25', 160)], ('ORD', 'LGA'): [('6:05', '8:32', 174), ('8:25', '10:34', 157), ('9:42', '11:32', 169), ('11:01', '12:39', 260), ('12:44', '14:17', 134), ('14:22', '16:32', 126), ('15:58', '18:40', 173), ('16:43', '19:00', 246), ('18:48', '21:45', 246), ('19:50', '22:24', 269)], ('MIA', 'LGA'): [('6:25', '9:30', 335), ('7:34', '9:40', 324), ('9:15', '12:29', 225), ('11:28', '14:40', 248), ('12:05', '15:30', 330), ('14:01', '17:24', 338), ('15:34', '18:11', 326), ('17:07', '20:04', 291), ('18:23', '21:35', 134), ('19:53', '22:21', 173)], ('BOS', 'LGA'): [('6:17', '8:26', 89), ('8:04', '10:11', 95), ('9:45', '11:50', 172), ('11:16', '13:29', 83), ('12:34', '15:02', 109), ('13:40', '15:37', 138), ('15:27', '17:18', 151), ('17:11', '18:30', 108), ('18:34', '19:36', 136), ('20:17', '22:22', 102)]}


    domain = []
    for people in peoples:
        domain.append(len(flights[(people[1], destination)]) - 1)
        domain.append(len(flights[(destination, people[1])]) - 1)
    #print 'domain=',domain



    # result, score = random_optimize(domain, schedule_cost)
    # print 'random_optimize result=',result, 'score=',score
    # 
    # result, score = hill_climb(domain, schedule_cost)
    # print 'hill_climb result=',result, 'score=',score
    # 
    # result, score = annealing_optimize(domain, schedule_cost)
    # print 'annealing_optimize result=',result, 'score=',score
    # 
    # result, score =  genetic_optimize(domain, schedule_cost)
    # print 'genetic_optimize result=',result, 'score=',score


    print '***************************************'


    # Двухместные комнаты
    dorms = ['Zeus','Athena','Hercules','Bacchus','Pluto']
    dormss = ['0 Zeus','1 Athena','2 Hercules','3 Bacchus','4 Pluto']

    # Люди и два пожелания у каждого (основное, второстепенное)
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

    #  список отсеков, т.е. первые 2 места - 0 отсек и т.д.
    slots = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
    slotss = ['0 0 Zeus', '1 0 Zeus', '2 1 Athena', '3 1 Athena', '4 2 Hercules', '5 2 Hercules', '6 3 Bacchus', '7 3 Bacchus', '8 4 Pluto', '9 4 Pluto']

    # [9, 8, 7, 6,..., 1]
    domain = [i for i in xrange(9, 0, -1)]

    print 'domain=',domain
    pprint (prefs)
    print 'dorms=',dorms
    print 'dormss=',dormss
    pprint (slots)
    print slotss

    #i = 0
    #for pr in prefs:
    #    print i,pr[i]
    #    i += 1

    print '***************************************'
    result, score = random_opt(domain, dorm_cost_)
    print 'random_optimize dorm_cost result=',result, 'score=',score

    print '***************************************'
    i = 0
    for x in result:
        dorm = dorms[slots[int(x)]]
        pref = prefs[i][1]
        print i,x,int(x), '->', slots[int(x)],'->', prefs[i][0], pref, '->', dorm
        i += 1


    # print '***************************************'
    # result, score = annealing_optimize(domain, dorm_cost)
    # print 'annealing_optimize dorm_cost result=',result, 'score=',score
    # 
    # print '***************************************'
    # i = 0
    # for x in result:
    #     dorm = dorms[slots[x]]
    #     pref = prefs[i][1]
    #     print x, '->', slots[x],'->', prefs[i][0], pref, '->', dorm
    #     i += 1
    # 
    print '***************************************'
    result, score = genetic_opt(domain, dorm_cost)
    print 'genetic_optimize dorm_cost result=',result, 'score=',score
    print i,x, '->', slots[x],'->', prefs[i][0], pref, '->', dorm
    
    print '***************************************'
    i = 0
    for x in result:
        dorm = dorms[slots[x]]
        pref = prefs[i][1]
        print i,x, '->', slots[x],'->', prefs[i][0], pref, '->', dorm
        i += 1

    ### ERR
    ###result, score = hill_climb(domain, dorm_cost)
    ###print 'hill_climb dorm_cost  result=',result, 'score=',score

    sys.exit(0)



#-------------------------------------------------------------------------------
# main module stub to prevent auto execute
#

if __name__ == '__main__':
    print "main_cds_1.py"
    akaMain(sys.argv)
    sys.exit(0)

