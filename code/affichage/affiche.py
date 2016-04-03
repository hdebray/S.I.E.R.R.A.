# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 14:46:02 2016

@author: ogustin
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as col
import matplotlib.cm as cm

import warnings as war      #permet de gérer les warning comme des error
import os
import subprocess

war.filterwarnings("ignore",category=RuntimeWarning)

"""
Création d'une carte de couleur continue linéaire, à partir d'une série de valeurs RGB
"""
color_map = { 'red': ((0.0, 0.007, 0.007),
                      (0.25, 0.035, 0.035),
                      (0.49, 0.067, 0.067),
                      (0.5, 0.271, 0.271),
                      (0.51, 0.165, 0.165),
                      (0.75, 0.451, 0.451),
                      (0.85, 0.6, 0.6),
                      (0.95, 0.7, 0.7),
                      (1.0, 1.0, 1.0)),
            'green': ((0.0, 0.168, 0.168),
                      (0.25, 0.243, 0.243),
                      (0.49, 0.322, 0.322),
                      (0.5, 0.424, 0.424),
                      (0.51, 0.4, 0.4),
                      (0.75, 0.5, 0.5),
                      (0.85, 0.561, 0.561),
                      (0.95, 0.702, 0.702),
                      (1.0, 1.0, 1.0)),
             'blue': ((0.0, 0.267, 0.267),
                      (0.25, 0.361, 0.361),
                      (0.49, 0.439, 0.439),
                      (0.5, 0.463, 0.463),
                      (0.51, 0.161, 0.161),
                      (0.75, 0.302, 0.302),
                      (0.85, 0.361, 0.361),
                      (0.95, 0.702, 0.702),
                      (1.0, 1.0, 1.0))}
                      
earth_color = col.LinearSegmentedColormap('earth',color_map,N=256)

"""
Création d'une carte de couleurs finies par valeurs discrètes, en code hexadécimal
"""
cpool = ['#2a0d03','#0085ff', '#00e503', '#4e8539', '#b6aba2', 
         '#dc6741', '#d44212', '#a9340e', '#7f270a', '#541a07']
         
"""Sauvegarde des couleurs de simulation, une par intensité maximale sur la carte"""
sim_0 = col.ListedColormap(cpool[1:5], 'indexed')       #pas de feu
cm.register_cmap(cmap=sim_0)
sim_1 = col.ListedColormap(cpool[1:6], 'indexed')       #intensité max = 1
cm.register_cmap(cmap=sim_1)
sim_2 = col.ListedColormap(cpool[1:7], 'indexed')       #intensité max = 2
cm.register_cmap(cmap=sim_2)
sim_3 = col.ListedColormap(cpool[1:8], 'indexed')       #intensité max = 3
cm.register_cmap(cmap=sim_3)
sim_4 = col.ListedColormap(cpool[1:9], 'indexed')       #intensité max = 4
cm.register_cmap(cmap=sim_4)
sim_5 = col.ListedColormap(cpool[1:10], 'indexed')       #intensité max = 5
cm.register_cmap(cmap=sim_5)

"""Couleurs utilisés si il y a des cases carbonisées"""
sim_0_c = col.ListedColormap(cpool[0:5], 'indexed')
cm.register_cmap(cmap=sim_0_c)
sim_1_c = col.ListedColormap(cpool[0:6], 'indexed')
cm.register_cmap(cmap=sim_1_c)
sim_2_c = col.ListedColormap(cpool[0:7], 'indexed')
cm.register_cmap(cmap=sim_2_c)
sim_3_c = col.ListedColormap(cpool[0:8], 'indexed')
cm.register_cmap(cmap=sim_3_c)
sim_4_c = col.ListedColormap(cpool[0:9], 'indexed')
cm.register_cmap(cmap=sim_4_c)
sim_5_c = col.ListedColormap(cpool[0:10], 'indexed')
cm.register_cmap(cmap=sim_5_c)

def dessine(carte,nom=''):
    """Affichage de la carte sous forme d'une matrice avec la fonction matshow
    La variable 'nom' permet de sauvegarder l'image sous un nom différent"""
    carbo = carte.calcul_mat()      #mise à jour de lamatrice en fonction des cases, renvoie un booléen pour les cases carbo
    mx = np.amax(carte.carte)       #maximum de valeur dans la matrice, pour déterminer la carte de couleur
        
    if(carbo == False):
        if(mx <= 3.0): couleur = sim_0
        elif(mx == 4.0): couleur = sim_1
        elif(mx == 5.0): couleur = sim_2
        elif(mx == 6.0): couleur = sim_3
        elif(mx == 7.0): couleur = sim_4
        elif(mx == 8.0): couleur = sim_5
    else:       #on utilise les couleurs spécifiques au cas "carbonisé"
        if(mx <= 3.0): couleur = sim_0_c
        elif(mx == 4.0): couleur = sim_1_c
        elif(mx == 5.0): couleur = sim_2_c
        elif(mx == 6.0): couleur = sim_3_c
        elif(mx == 7.0): couleur = sim_4_c
        elif(mx == 8.0): couleur = sim_5_c
        else: print(mx,carbo)
        
    plt.ioff()         #empêche l'affichage des images
        
    plt.matshow(carte.carte,cmap=couleur)
    #plt.colorbar()     #affiche le code couleur utilisé
        
    for pompier in carte.liste_pompier:     #affiche toute les pompiers avec un carré rouge de 5 pixels
        plt.plot(pompier.x,pompier.y,'rs',markersize=5)
        
    plt.axis([-0.5,carte.taille-0.5,-0.5,carte.taille-0.5])     #cadre l'image et cache les axes
    plt.axis('off')
        
    txt = "img" + str(carte.iter+10) + nom + ".png"      #nom de l'image
    plt.savefig(txt,dpi=100,bbox_inches='tight',pad_inches=0)


def compiler():
    """Permet de convertir la liste d'images en un gif, puis supprime les images créé
    Il est nécéssaire d'installer Imagemagick pour convertir, ainsi que de sauvegarder les png à la racine
    """
    
#    args = ['convert', '*.png', 'toto.gif']
#    subprocess.call(args,shell=True)
    
    os.system('convert -delay 50 -loop 0 *.png simulation.gif')
    
    os.system('del *.png')    # destruction des images
    
    