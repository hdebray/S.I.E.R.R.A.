# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 15:20:49 2016

@author: Amaury
"""
import numpy as np
import random as rdm

def distance(x1,y1,x2,y2):  #Peut-être utiliser la distance de Manhattan ? |xb - xa| + |yb - ya|
"""Calcul de la distance euclidienne entre deux points 1 et 2"""
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)


class Pompier(object):
    def __init__(self,nom,x,y):
        self.nom = str(nom)
        self.x = x
        self.y = y
        
    def deplacement(self,autre):
        """Déplacement d'un pompier vers une autre case"""
        if self.x < autre.x and self.y < autre.y:
            self.x,self.y = self.x+1,self.y+1
        elif self.x > autre.x and self.y > autre.y:
            self.x,self.y = self.x-1,self.y-1
        elif self.x < autre.x and self.y > autre.y:
            self.x,self.y = self.x+1,self.y-1
        elif self.x > autre.x and self.y < autre.y:
            self.x,self.y = self.x-1,self.y-1
        elif self.x > autre.x and self.y == autre.y:
            self.x = self.x-1
        elif self.x == autre.x and self.y < autre.y:
            self.y = self.y+1
        elif self.x == autre.x and self.y > autre.y:
            self.y = self.y-1
        elif self.x > autre.x and self.y == autre.y:
            self.x = self.x+1
        
        
    def agir(self,carte,liste_brule):
        case_perso = carte.recherche(self.x,self.y)     #case qui correspond à la position du pompier
        adj = case_perso.adjacence(carte)               #liste des cases adjacentes à celle du pompier
        
        objectif = self.cherche_feu(liste_brule)        #cherche les cases qui brulent
        if(objectif != None):
            self.aller_vers_feu(case_perso,adj,objectif,carte)        #le pompier se déplace
            
            case_perso = carte.recherche(self.x,self.y)
            adj = case_perso.adjacence(carte)
            nouv_liste_brule = self.eteindre_feu(case_perso,adj,liste_brule)        #le pompier éteint le feu
            
        else: nouv_liste_brule = liste_brule
            
        return nouv_liste_brule
            
        
    def cherche_feu(self,liste_brule):
        """Cherche la case qui brule la plus proche du pompier, selon la distance entre chaque case qui brule"""
        dist = float('inf')
        case = None
        
        for cell in liste_brule:        #parcourt la liste des cases en feu
            temp = distance(self.x,self.y, cell.x,cell.y)
            if temp < dist:     #si la distance est plus courte, le pompier voit choisir cette case
                dist = temp
                case = cell
        return case
            
            
    def aller_vers_feu(self,case,adjacentes,case_feu,carte):
        if case.etat > 0:       #si la case du pompier est en feu, il s'en écarte 
            issue = case
            for cell in adjacentes:
                if cell.etat < issue.etat:
                    issue = cell
            self.deplacement(issue)     #déplacement en direction de l'issue
        
        else:
            bouge = True        #booléen pour savoir si pompier va bouger ou non
            for cell in adjacentes:
                if(case_feu == cell): bouge = False     #si la case objectif est adjacentes, le pompier ne se déplace pas
            
            if(bouge): self.deplacement(case_feu)     #déplacement en direction du feu
                  

    def eteindre_feu(self,case,liste_adj,liste_brule):
        brule = []      #liste des cellules adjacentes qui brulent
        for cell in liste_adj:
            if(cell.etat > 0 and cell.carbo == False):      #si la case brule, mais n'est pas cramé
                brule.append(cell)
                
        if(len(brule) <= 3):        #si il y a moins de 3 cases en feu autour
            for cell in brule:
                cell.etat -= 2              #on éteint la case
                if(cell.etat < 0): cell.etat = 0  #l'intensité du feu n'est pas inférieure à 0
                if(cell.etat == 0): liste_brule.remove(cell)
                
        else:
            for i in range(len(brule)):
                r = rdm.randint(0,len(brule))       #choix aléatoire de la case à éteindre, parmis celles disponibles
                cell = brule[r]
                cell.etat -= 2
                if(cell.etat < 0): cell.etat = 0
                if(cell.etat == 0):
                    liste_brule.remove(cell)
                    brule.remove(brule[r])      #on retire la case qui vient d'etre éteinte
        return liste_brule