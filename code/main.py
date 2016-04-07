# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 10:26:48 2016

@author: ogustin
"""

import matplotlib.pyplot as plt
import numpy as np

import base.map as map
import base.cell as cl
import base.fireman as frm
import gui.display as disp


"""
TO DO list:
-test every functions independantly
-create a beautiful interface (NOT Tkinter!)
-implement functions to save and restore the simulation state on db
"""


"""Tests of the Fireman class"""
gus = frm.Fireman('Augustin',0,0)       #create a fireman
#print(gus)

"""Tests of the Cell class"""


"""Tests of the Map class"""
map = map.Map(30)     #init a map (should be size < 500, or take a coffee while waiting for the result)

#height = map.heightmap()      #test the creation of a heightmap
#plt.matshow(height,cmap='gray')

map.creation()        #create the map for the simulation
map.ini()             #initiate the number of burning cells, and firemans

#for p in map.liste_fireman:      #display the firemen
#    print(p)

#for c in map.liste_cell:     #display every Case object
#    print(c)
    
#for b in map.burn_list:     #display every Case object on fire
#    print(b)


disp.draw(map)       #display the initial state of the simulation
i=0
while(len(map.burn_list) > 0):
    map.turn()
    
    i+=1
    if(i>5*map.size):break      #seatbelt, to prevent accidents

disp.compile(delete=True)       #transform png to gif   !! Imagemagick necessary !!
