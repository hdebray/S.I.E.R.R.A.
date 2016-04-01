# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 11:49:48 2016

@author: ogustin
"""

import numpy as np
import random as rnd

import metier.pompier as pom
import metier.case as cs
import affichage.affiche as af
import bdd.donnee as bd

    


"""
Création d'une carte en combinant deux cartes de hauteur (heightmap), 
générées par un bruit de valeur (Value Noise)
"""
class Carte(object):
    def __init__(self,taille):
        self.taille = taille
        self.carte = np.zeros([taille,taille])
        self.liste_case = []        #liste des cases qui composent la carte
        self.liste_brule = []       #liste des cases en train de bruler à chaque itération
        self.liste_pompier = []     #liste des pompiers actifs sur la carte
        self.iter = 0               #numéro de l'itération au cours de la simulation
        
        
    def creation(self):
        """Combine deux heightmap (altitude et humidité), puis construit la carte qui en dépend"""
        alti = self.heightmap()
        foret = self.heightmap()
        for i in range(self.taille):
            for j in range(self.taille):
                self.carte[i,j] = self.biome(alti,foret,i,j)        #créé la carte
        
                
    def biome(self,alti,foret,i,j):
        """Construit la carte en combinant les valeurs des deux heightmap"""
        n = 0
        if(alti[i,j] < 0.3):        #eau
            n = 0
            self.liste_case.append(cs.Case(j,i,0))
        elif(alti[i,j] > 0.6 and foret[i,j] > 0.5):     #foret
            n = 2
            self.liste_case.append(cs.Case(j,i,2))
        elif(alti[i,j] > 0.7 and foret[i,j] < 0.4):     #maison
            n = 3
            self.liste_case.append(cs.Case(j,i,3))
        else:               #plaine
            n = 1
            self.liste_case.append(cs.Case(j,i,1))
        return n
        
    def heightmap(self,amp=1,freq=1/2.0):
        """Construit une heightmap en ajoutant successivement des bruits de valeurs,
        à des amplitudes et des fréquences différentes"""
        bruit = np.zeros([self.taille,self.taille])     #initialisation
        while(self.taille*freq > 1 and amp > 0.01):     #tant que la résolution de la carte est supérieur à 1
            bruit += self.calc_bruit(self.taille*freq) * amp
            freq *= 0.4     #augmentation de la fréquence
            amp *= 0.6    #diminution de l'amplitude
        bruit = self.distrib(bruit)
        return bruit
        
    def calc_bruit(self,res):
        """Calcul un bruit de valeur pour une résolution données (taille*fréquence).
        La graine utilisé pour générer le bruit blanc de départ est différente à chaque fois"""
        perm = np.random.permutation(256)           #table de permutation aléatoire (graine du monde)
        self.blanc = self.bruit_blanc(self.taille,perm)                #bruit blanc
        
        temp = np.zeros([self.taille,self.taille])
        for i in range(self.taille):
            for j in range(self.taille):
                m,n = int(i/res),int(j/res)
                temp[i][j] = self.lissage(i/res,j/res)      #interpolation lissée du bruit blanc
                
        return temp
        
    def lissage(self,y,x):
        """Cette fonction lisse l'interpolation pour avoir un meilleur résultat, en utilisant
        une interpolation bilinéaire"""
        x0 = int(x)         #partie entière
        frac_x = x - x0     #partie fractionnaire
        y0 = int(y)
        frac_y = y - y0
        
        x1 = (x0+1)
        y1 = (y0+1)
        if(x1 > len(self.blanc)-1): x1 = len(self.blanc)-1
        if(y1 > len(self.blanc)-1): y1 = len(self.blanc)-1
        
        dx1 = self.lerp(frac_x,self.blanc[y0][x0],self.blanc[y0][x1])        #interpolation bilinéaire de la valeur du pixel
        dx2 = self.lerp(frac_x,self.blanc[y1][x0],self.blanc[y1][x1])
        result = self.lerp(frac_y,dx1,dx2)
        return result
        
    def lerp(self,p,a,b):
        """Interpolation linéaire de la valeur en p, selon la valeur au point a et au point b"""
        t = (p**2)*(3 - 2*p)          #lissage de l'interpolation, cubique 
        return a*(1-t) + b*t        #interpolation
        
    def bruit_blanc(self,dim,perm):
        """Génération d'un bruit blanc, selon une graine (table de permutation)"""
        mat = np.zeros([dim,dim])
        for i in range(dim):
            for j in range(dim):
                mat[i][j] = perm[ (j%256 + perm[i%256]) % 256 ]
        return mat

    def distrib(self,mat):
        """Redistribue les valeurs d'une matrice entre 0 et 1"""
        mx,mn = np.ceil(np.amax(mat)),np.floor(np.amin(mat))
        result = (mat-mn)/(mx-mn)
        return result
        
        
    """
    Modification et mise à jour de l'état de la simulation
    """
    def ini(self,foyer=-1,pompier=-1):
        if(foyer < 0): foyer = int(self.taille/10)
        self.johny(foyer)           #allumer le feu
        if(pompier < 0): pompier = int(self.taille/4)
        self.creer_pompier(pompier)     #créer les pompiers
        
    def tour(self):
        if(self.iter == 0 and len(self.liste_brule) < 1): self.ini()     #initialisation si cela n'a pas été fait
        self.iter+= 1
        
        k = len(self.liste_brule)
        i = 0
        while(i < k):
            if(len(self.liste_brule) > 0):
                cell = self.cherche(self.liste_brule[i].x,self.liste_brule[i].y)        #on récupère la cellule qui va être propagé 
                cell.propagation(self)
                if(cell.carbo == True): k -= 1      #si la case vient d'être carbonisé, la taille de liste_brule a diminué
                
                i += 1
                
        af.dessine(self,'a')
        
        for pmp in self.liste_pompier:
            pmp.agir(self)
            
        af.dessine(self,'b')
            
    
    def johny(self,n):
        """ ALLUMMEEEEEEEEEEEEEEEERR,  LE FEEUUU !! """
        for i in range(n):      #n: nombre de foyer de feu au début de la simulation
            b = True
            while(b):           #boucle de test pour ne pas bruler l'eau
                b = False
                x,y = rnd.randint(0,self.taille-1),rnd.randint(0,self.taille-1)
                case = self.cherche(x,y)
                if(case.nat == 0): b = True
            case.etat = 1
            self.liste_brule.append(case)
            
            
    def creer_pompier(self,n):
        for i in range(n):      #n: nombre de pompiers au début de la simulation
            nom = "august"+str(i)
            b = True
            while(b):           #boucle de test pour ne pas mettre un pompier dans l'eau
                b = False
                x,y = rnd.randint(0,self.taille-1),rnd.randint(0,self.taille-1)
                case = self.cherche(x,y)
                if(case.nat == 0 or case.etat > 0): b = True
            self.liste_pompier.append(pom.Pompier(nom,x,y))     #créer un nouveau pompier et l'ajoute à la liste
        
        
    def cherche(self,x,y):
        """Cette fonction cherche une case aux coordonnées x et y dans une liste d'objets Case"""
        result = None
        for case in self.liste_case:
            if(case.x == x and case.y == y): result = case
        return result
        
    def calcul_mat(self):
        """Cette fonction recalcule la matrice self.carte en fonction des cases, et indique si il y a
        des cases carbonisées. Elle n'est normalement utilisé que pour l'affichage"""
        self.carte = np.zeros([self.taille,self.taille])
        case_carbo = False      #booléen pour savoir si il y a des cases carbonisées dans la carte
        for cell in self.liste_brule:       #on affecte d'abord les cases en feu
            i,j = cell.y,cell.x
            self.carte[i,j] = 3 + cell.etat
        
        for cell in self.liste_case:
            i,j = cell.y,cell.x
            if(self.carte[i,j] == 0):       #si une valeur n'a pas déja été affecté
                    if(cell.carbo == True):     #si c'est une case carbo, on lui affecte le maximum +1 (pour l'affichage)
                        case_carbo = True
                        self.carte[i,j] = -1
                    else:
                        self.carte[i,j] = cell.nat      #sinon, on affecte le chiffre correspondant à la nature
        return case_carbo
        
        
    def sauvegarde(self):
        """Sauvegarde l'état actuel de la matrice"""
        bd.sauve_carte(self.liste_case,self.iter)
        