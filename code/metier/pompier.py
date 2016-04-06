# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 15:20:49 2016
@author: Amaury
"""
import numpy as np
import random as rdm

def distance(x1,y1,x2,y2):  
    """Calcul de la distance euclidienne entre deux points 1 et 2"""
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)


class Pompier(object):
    def __init__(self,nom,x,y):
        self.nom = str(nom)     #le nom sertd'identifiant
        self.x = x              #coordonnées
        self.y = y
        self.pv = 20
        
    def __str__(self):
        return "{}".format(self.nom)
        
    def deplacement(self,autre,n):
        """Déplacement d'un pompier vers une autre case"""
        if self.x < autre.x and self.y < autre.y:
            self.x,self.y = self.x+n,self.y+n
        elif self.x < autre.x and self.y > autre.y:
            self.x,self.y = self.x+n,self.y-n
        elif self.x > autre.x and self.y > autre.y:
            self.x,self.y = self.x-n,self.y-n
        elif self.x > autre.x and self.y < autre.y:
            self.x,self.y = self.x-n,self.y+n
        elif self.x > autre.x and self.y == autre.y:
            self.x = self.x-n
        elif self.x < autre.x and self.y == autre.y:
            self.x = self.x+n
        elif self.x == autre.x and self.y > autre.y:
            self.y = self.y-n
        elif self.x == autre.x and self.y < autre.y:
            self.y = self.y+n
        
        
    def agir(self,carte):
        """Méthode principale du pompier, pour appeler les autre fonctions"""
        case_perso = carte.cherche(self.x,self.y)     #case qui correspond à la position du pompier
        adj = case_perso.adjacence(carte)               #liste des cases adjacentes à celle du pompier
        
        objectif = self.cherche_feu(carte.liste_brule)        #cherche les cases qui brulent
        if(objectif != None):
            deplacement = True
            for case in adj:        #on cherche si le pompier est à coté du feu
                if(case.x == objectif.x and case.y == objectif.y): deplacement = False
                
            if(deplacement):
                self.aller_vers_feu(case_perso,adj,objectif)        #le pompier se déplace
            else:
                self.eteindre_feu(case_perso,adj,carte)        #le pompier éteint le feu

        
    def cherche_feu(self,liste_brule):
        """Cherche la case qui brule la plus proche du pompier, selon la distance entre chaque case qui brule"""
        dist = float('inf')
        case = None
        
        for cell in liste_brule:        #parcourt la liste des cases en feu
            temp = distance(self.x,self.y, cell.x,cell.y)
            if temp < dist:     #si la distance est plus courte, le pompier va choisir cette case
                dist = temp
                case = cell
        return case
            
            
    def aller_vers_feu(self,case,liste_adj,case_feu):
        """Gère le déplacement du pompier en fonction de sa position et de la position de la case en feu"""
        if(case.etat > 0): self.pv -= case.etat                #le pompier est brulé d'un montant égal à l'intensité
        
        if(case.etat > 0 and case.carbo != True):       #si la case du pompier est en feu, il s'en écarte
            issue = case
            for cell in liste_adj:
                if cell.etat < issue.etat:      #on cherche la case à l'intensité la plus faible
                    issue = cell
            self.deplacement(issue)             #déplacement en direction de l'issue
        
        else:
            bouge = True        #booléen pour savoir si pompier va bouger ou non
            for cell in liste_adj:
                if(case_feu.x == cell.x and case_feu.y == cell.y): bouge = False     #si la case objectif est adjacentes, le pompier ne se déplace pas
            
            if(bouge):
                if distance(self.x,self.y,case_feu.x,case_feu.y)>=4:
                    self.deplacement(case_feu,2)     #déplacement en direction du feu en courant si on est loin
                else:
                    self.deplacement(case_feu,1)     #déplacement en direction du feu en marchant si on est proche
                    
                    
    def eteindre_feu(self,case,liste_adj,carte):
        """Calcul les cases adjacentes qui peuvent être éteintes à partir de la position actuelle du pompier"""
        brule = []      #liste des cellules adjacentes qui brulent
        for cell in liste_adj:
            if(cell.etat > 0 and cell.carbo == False):      #si la case brule, mais n'est pas cramé
                brule.append(cell)
                
        if(len(brule) <= 3):        #si il y a moins de 3 cases en feu autour
            for cell in brule:
                cell.etat -= 2              #on éteint la case
                if(cell.etat < 0): cell.etat = 0  #l'intensité du feu n'est pas inférieure à 0
                if(cell.etat == 0): carte.liste_brule.remove(cell)
                
        else:
            k=len(brule)
            i=0
            while i < k:
                r = rdm.randint(0,len(brule)-1)       #choix aléatoire de la case à éteindre, parmis celles disponibles
                cell = brule[r]
                cell.etat -= 2
                if(cell.etat < 0): cell.etat = 0
                if(cell.etat == 0):
                    carte.liste_brule.remove(cell)
                    brule.remove(brule[r])      #on retire la case qui vient d'etre éteinte
                    
                i+=1
                k=len(brule)
