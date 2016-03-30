# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 09:53:14 2016

@author: Henri
"""
import numpy as np
import random as rdm
#eau=0; plaine=1; foret=2; maison=3
#case(x,y,nature,état,carbonisée)
# le terrain est une matrice (chaque case se définit pars ses coordonnées, son type, son état, si elle est carbonisée), liste_brulee est la liste des coordonnées des cases brulées)



def coordonnées2case(x,y,carte):
    return carte(x,y)

class Case(object):
    def __init__(self,x,y,nat,etat=0,carbo=False):
        self.x=x
        self.y=y
        self.nat=nat
        self.etat=etat
        self.carbo=carbo
        

            
    def adjacence(self,carte):
        adjacentes=[]
        for i in range(self.x-1,self.x+2):
            for j in range(self.y-1,self.y+2):
                if i>=0 and i<len(carte) and j>=0 and j<len(carte):
                    adjacentes.append(coordonnées2case(i,j,carte))
        return adjacentes
        
        
    
    def propagation(self):
        nature=self.nat
        n=rdm.randint(0,état)
        état=self.etat
        charbon=self.carbo
        brulables=[]
        adj=self.adjacence()
        for i in range(len(adj)):
            case_adj=adj[i]
            if case_adj.nat==1 or case_adj.nat==2 or case_adj.nat==3:
                if case_adj.carbo==False and case_adj.etat==0:
                    brulables.append(case_adj)
        if nature==1 or nature==3:
            n=rdm.randint(0,état)
                
        if nature==2:
            n=rdm.randint(0,(état*2))
            if n>8:
                n=8
        if n>=len(brulables):
            for case in brulables:
                brulable(case).etat=1
        else:
            case_a_bru=[]
            while len(indices)<n:
                position=rdm.randint(0,len(brulables))
                for indice in case_a_bru:
                    if position!=case_a_bru[indice]:
                        case_a_bru.append(ind)
            
            
            for case in case_a_bru:
                case_a_bru(case).etat=1
    
    
    
    
