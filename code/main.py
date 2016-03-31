# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 10:26:48 2016

@author: ogustin
"""

import matplotlib.pyplot as plt

import metier.carte as crt
import metier.case as cs
import metier.pompier as pom
import affichage.affiche as af


"""Test sur l'objet Pompier"""
gus = pom.Pompier('Augustin',0,0)       #créer un pompier
#print(gus)

"""Test sur l'objet Case"""


"""Test sur l'objet Carte"""
carte = crt.Carte(10)     #initialise une carte (ne pas dépasser une taille de 500, sinon calcul trop long)

#bruit = carte.heightmap()      #test sur la création d'un seul bruit de valeur
#plt.matshow(bruit,cmap='gray')

carte.creation()        #création de la carte de simulation
carte.ini(1,2)

#for p in carte.liste_pompier:      #affiche les pompiers
#    print(p)

#for c in carte.liste_case:     #affiche les objets Cases de la simulation
#    print(c)
    
#for b in carte.liste_brule:     #affiche les objets Cases qui sont en feu
#    print(b)


af.dessine(carte)       #affichage de l'état initial

for i in range(2):      #réalise deux tours de simulation
    carte.tour()
    