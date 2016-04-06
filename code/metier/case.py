# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 09:53:14 2016

@author: Henri
"""

import random as rdm

"""
Convention: eau=0; plaine=1; foret=2; maison=3
cell(x,y,nature,état,charrednisée)
le terrain est une matrice (chaque cell se définit pars ses coordonnées, son type, son état, si elle est charrednisée), burn_liste est la liste des coordonnées des cells brulées)
"""

class Cell(object):
    def __init__(self,x,y,nat,state=0,charred=False):
        self.x = x
        self.y = y
        self.nat = nat
        self.state = state
        self.charred = charred
        
    def __str__(self):
        if(self.nat == 0): txt = 'water'
        if(self.nat == 1): txt = 'grass'
        if(self.nat == 2): txt = 'forest'
        if(self.nat == 3): txt = 'town'
        
        return "{} (x:{},y:{})".format(txt,self.x,self.y)
            
    def get_near(self,map):
        """Cette fonction récupère la liste des cells near_cells à elle-même, sauf elle-même"""
        near_cells = []
        for i in range(self.x-1, self.x+2):
            for j in range(self.y-1, self.y+2):
                #if(i == j): continue
                if(i>=0 and i<map.size and j>=0 and j<map.size): near_cells.append(map.cherche(i,j))
        return near_cells
        
        
    
    def propagation(self,map):
        """La fonction permet de calculer la propagation du feu, à partir d'une cellule vers les near_cells"""
        near_cells = self.get_near(map)
        
        #propagation du feu
        burnable = []                  #liste des cells où le feu peut se propager
        for cell in near_cells:
            if(cell.nat != 0 and cell.state == 0):  #conditions pour bruler une cell
                burnable.append(cell)
                
        if(self.nat == 2):                          #si c'est un arbre, la propagation est doublé
            n = rdm.randint(0,(self.state*2))        #n: nombre de cells à bruler
            if n>8: n=8                             #ne peut pas dépasser 8
        else: n = rdm.randint(0,self.state)
        
        if n>=len(burnable):               #si il y a plus de cells à bruler que de cells burnable, elles sont toutes brulé
            for cell in burnable:
                cell.state = 1
                map.burn_list.append(cell)      #ajout de la cell à burn_list
        else:                
            for i in range(n):
                r = rdm.randint(0,len(burnable)-1)   #choix aléatoire de la cell à bruler, parmis celles disponibles
                cell = burnable[r]
                cell.state = 1                       #on brule la cell
                map.burn_list.append(cell)
                burnable.remove(cell)      #la cell ne fait plus partie des cells burnable
                
        #augmentation de l'intensité        
        if(self.nat == 3 and self.charred == False):  #si c'est une maison, intensité + 2
            self.state += 2
        else:
            self.state += 1      #sinon, intensité + 1
            
        if(self.state > 5):      #cas "charrednisé"
            self.charred = True
            self.state = 1
            map.burn_list.remove(self)      #les cells charrednisé ne font plus parties de la liste des cells en feu
            