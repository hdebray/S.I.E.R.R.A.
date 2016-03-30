# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 15:20:49 2016

@author: Amaury
"""
import numpy as np


def distance(x1,y1,x2,y2):
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)


class Pompier(object):
    
    def __init__(self,nom,x,y):
        
        self.nom=nom
        self.x=x
        self.y=y
        
    def deplacement(self,dx,dy):
        self.x += dx
        self.y += dy
        
    def cherche_feu(self,liste_brule):
        x=self.x
        y=self.y
        dist=float('inf')
        cellule=liste_brule[0]
        
        for cell in liste_brule:
            temp = distance(x,y, cell.x,cell.y)
            if temp < dist:
                dist = temp
                cellule=cell
        
        return cellule
            
        