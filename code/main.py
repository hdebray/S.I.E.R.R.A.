# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 10:26:48 2016

@author: ogustin
"""

import matplotlib.pyplot as plt
import numpy as np

import metier.map as map
import metier.cell as cl
import metier.fireman as frm
import affichage.display as disp


"""
A faire:
-gif avec les images successives
-tester toute les 'briques élémentaires'
"""


"""Test sur l'objet Fireman"""
gus = frm.Fireman('Augustin',0,0)       #créé un fireman
#print(gus)

"""Test sur l'objet Case"""


"""Test sur l'objet Map"""
map = map.Map(10)     #initialise une map (ne pas dépasser une size de 500, sinon calcul trop long)

#bruit = map.heightmap()      #test sur la création d'un seul bruit de valeur
#plt.matshow(bruit,cmap='gray')

map.creation()        #création de la map de simulation
map.ini()             #initialisation du nombre de feu, et du nombre de firemans

#for p in map.liste_fireman:      #display les firemans
#    print(p)

#for c in map.liste_cell:     #display les objets Cases de la simulation
#    print(c)
    
#for b in map.burn_list:     #display les objets Cases qui sont en feu
#    print(b)


disp.draw(map)       #dispfichage de l'état initial
i=0
while(len(map.burn_list) > 0):      #réalise deux turns de simulation
    map.turn()
    
    i+=1
    if(i>4*map.size):break      #ceinture de sécurité

disp.compile(delete=True)       #transforme les images en gif   !! Imagemagick nécéssaire !!