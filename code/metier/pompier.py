# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 15:20:49 2016

@author: Amaury
"""

class Pompier(object):
    
    def __init__(self,nom,x,y):
        
        self.nom=nom
        self.x=x
        self.y=y
        
    def deplacement(self,dx,dy):
        self.x += dx
        self.y += dy
        
    
    