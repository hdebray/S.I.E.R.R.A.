# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 09:53:14 2016

@author: Henri
"""

import random as rdm

"""
Convention: eau=0; plaine=1; foret=2; maison=3
case(x,y,nature,état,carbonisée)
le terrain est une matrice (chaque case se définit pars ses coordonnées, son type, son état, si elle est carbonisée), liste_brulee est la liste des coordonnées des cases brulées)
"""

class Case(object):
    def __init__(self,x,y,nat,etat=0,carbo=False):
        self.x = x
        self.y = y
        self.nat = nat
        self.etat = etat
        self.carbo = carbo
        
    def __str__(self):
        if(self.nat == 0): txt = 'eau'
        if(self.nat == 1): txt = 'plaine'
        if(self.nat == 2): txt = 'foret'
        if(self.nat == 3): txt = 'maison'
        
        return "{} (x:{},y:{})".format(txt,self.x,self.y)
            
    def adjacence(self,carte):
        """Cette fonction récupère la liste des cases adjacentes à elle-même, sauf elle-même"""
        adjacentes = []
        for i in range(self.x-1, self.x+2):
            for j in range(self.y-1, self.y+2):
                #if(i == j): continue
                if(i>=0 and i<carte.taille and j>=0 and j<carte.taille): adjacentes.append(carte.cherche(i,j))
        return adjacentes
        
        
    
    def propagation(self,carte):
        """La fonction permet de calculer la propagation du feu, à partir d'une cellule vers les adjacentes"""
        adj = self.adjacence(carte)
        
        #propagation du feu
        brulables = []                  #liste des cases où le feu peut se propager
        for cell in adj:
            if(cell.nat != 0 and cell.carbo == False and cell.etat == 0):  #conditions pour bruler une case
                brulables.append(cell)
                
        if(self.nat == 2):                          #si c'est un arbre, la propagation est doublé
            n = rdm.randint(0,(self.etat*2))        #n: nombre de cases à bruler
            if n>8: n=8                             #ne peut pas dépasser 8
        else: n = rdm.randint(0,self.etat)
        
        if n>=len(brulables):               #si il y a plus de cases à bruler que de cases brulables, elles sont toutes brulé
            for case in brulables:
                case.etat = 1
                carte.liste_brule.append(case)      #ajout de la case à liste_brule
        else:                
            for i in range(n):
                r = rdm.randint(0,len(brulables)-1)   #choix aléatoire de la case à bruler, parmis celles disponibles
                case = brulables[r]
                case.etat = 1                       #on brule la case
                carte.liste_brule.append(case)
                brulables.remove(case)      #la case ne fait plus partie des cases brulables
                
        #augmentation de l'intensité        
        if(self.nat == 3 and self.carbo == False):  #si c'est une maison, intensité + 2
            self.etat += 2
        else:
            self.etat += 1      #sinon, intensité + 1
            
        if(self.etat > 5):      #cas "carbonisé"
            self.carbo = True
            self.etat = 1
            carte.liste_brule.remove(self)      #les cases carbonisé ne font plus parties de la liste des cases en feu
            