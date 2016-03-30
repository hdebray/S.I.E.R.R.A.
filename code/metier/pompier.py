# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 15:20:49 2016

@author: Amaury
"""
import numpy as np
import random as rdm

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
        case=liste_brule[0]
        
        for cell in liste_brule:
            temp = distance(x,y, cell.x,cell.y)
            if temp < dist:
                dist = temp
                case=cell
        
        return case
            
            
    def aller_vers_feu(self,case_feu,carte):
        
        case=carte.cherche(self.x,self.y)
        adj=case.adjacence()
        
        if case.etat > 0:
            adj=case.adjacence()
            
            for cell in adj:
                if cell.nat != 0:
                    echappatoire=cell
                    break
            
            for cell in adj:
                if cell.etat < echappatoire.etat and echappatoire.nat != 0:
                    echappatoire=cell
            
            self.x=echappatoire.x
            self.y=echappatoire.y
        
        
        else:
            for cell in adj:
                if cell.etat > 0:
                    return case, adj
                
                
            if self.x < case_feu.x and self.y < case_feu.y:
                self.deplacement(1,1)
            elif self.x > case_feu.x and self.y > case_feu.y:
                self.deplacement(-1,-1)
            elif self.x < case_feu.x and self.y > case_feu.y:
                self.deplacement(1,-1)
            elif self.x > case_feu.x and self.y < case_feu.y:
                self.deplacement(-1,1)
            elif self.x > case_feu.x and self.y == case_feu.y:
                self.deplacement(-1,0)
            elif self.x == case_feu.x and self.y < case_feu.y:
                self.deplacement(0,1)
            elif self.x == case_feu.x and self.y > case_feu.y:
                self.deplacement(0,-1)
            elif self.x > case_feu.x and self.y == case_feu.y:
                self.deplacement(1,0)
                
            
        nouv_case=carte.cherche(self.x,self.y)
        adja=nouv_case.adjacence()
        
        return nouv_case, adja
    
    

    def eteindre_feu(self, case, liste_adj, liste_brule, carte):
        liste_crame=[]
        
        for cell in liste_adj:
            if cell.etat > 0 and not cell.carbo:
                liste_crame.append(cell)
                
        liste_eteint=[]
        while a < 3:
            test=rdm.randint(0,len(liste_crame)-1)
            liste_eteint.append(liste_crame[test])
            del liste_crame[test]
            a=len(liste_eteint)
            
        pass
        
        