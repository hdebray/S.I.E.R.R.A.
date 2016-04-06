# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 11:49:48 2016

@author: ogustin
"""

import numpy as np
import random as rnd

import metier.fireman as frm
import metier.cell as cl
import affichage.display as display
import bdd.data as db

    


"""
Création d'une map en combinant deux maps de hauteur (heightmap), 
générées par un noise de valeur (Value Noise)
"""
class Map(object):
    def __init__(self,size):
        self.size = size
        self.map = np.zeros([size,size])
        self.cell_list = []        #liste des cells qui composent la map
        self.burn_list = []       #liste des cells en train de bruler à chaque itération
        self.fireman_list = []     #liste des firemans actifs sur la map
        self.count = 0               #numéro de l'itération au cours de la simulation
        
        
    def creation(self):
        """Combine deux heightmap (altitude et humidité), puis construit la map qui en dépend"""
        alti = self.heightmap()
        forest = self.heightmap()
        for i in range(self.size):
            for j in range(self.size):
                self.map[i,j] = self.biome(alti,forest,i,j)        #créé la map
        
                
    def biome(self,alti,forest,i,j):
        """Construit la map en combinant les valeurs des deux heightmap"""
        n = 0
        if(alti[i,j] < 0.3):        #eau
            n = 0
            self.cell_list.append(cl.Cell(j,i,0))
        elif(alti[i,j] > 0.6 and forest[i,j] > 0.5):     #forest
            n = 2
            self.cell_list.append(cl.Cell(j,i,2))
        elif(alti[i,j] > 0.7 and forest[i,j] < 0.4):     #maison
            n = 3
            self.cell_list.append(cl.Cell(j,i,3))
        else:               #plaine
            n = 1
            self.cell_list.append(cl.Cell(j,i,1))
        return n
        
    def heightmap(self,amp=1,freq=1/2.0):
        """Construit une heightmap en ajoutant successivement des noises de valeurs,
        à des amplitudes et des fréquences différentes"""
        noise = np.zeros([self.size,self.size])     #initialisation
        while(self.size*freq > 1 and amp > 0.01):     #tant que la résolution de la map est supérieur à 1
            noise += self.calc_noise(self.size*freq) * amp
            freq *= 0.4     #augmentation de la fréquence
            amp *= 0.6    #diminution de l'amplitude
        noise = self.distrib(noise)
        return noise
        
    def calc_noise(self,res):
        """Calcul un noise de valeur pour une résolution données (size*fréquence).
        La graine utilisé pour générer le noise white de départ est différente à chaque fois"""
        perm = np.random.permutation(256)           #table de permutation aléatoire (graine du monde)
        self.white = self.white_noise(self.size,perm)                #noise white
        
        temp = np.zeros([self.size,self.size])
        for i in range(self.size):
            for j in range(self.size):
                m,n = int(i/res),int(j/res)
                temp[i][j] = self.smooth(i/res,j/res)      #interpolation lissée du noise white
                
        return temp
        
    def smooth(self,y,x):
        """Cette fonction lisse l'interpolation pour avoir un meilleur résultat, en utilisant
        une interpolation bilinéaire"""
        x0 = int(x)         #partie entière
        frac_x = x - x0     #partie fractionnaire
        y0 = int(y)
        frac_y = y - y0
        
        x1 = (x0+1)
        y1 = (y0+1)
        if(x1 > len(self.white)-1): x1 = len(self.white)-1
        if(y1 > len(self.white)-1): y1 = len(self.white)-1
        
        dx1 = self.lerp(frac_x,self.white[y0][x0],self.white[y0][x1])        #interpolation bilinéaire de la valeur du pixel
        dx2 = self.lerp(frac_x,self.white[y1][x0],self.white[y1][x1])
        result = self.lerp(frac_y,dx1,dx2)
        return result
        
    def lerp(self,p,a,b):
        """Interpolation linéaire de la valeur en p, selon la valeur au point a et au point b"""
        t = (p**2)*(3 - 2*p)          #smooth de l'interpolation, cubique 
        return a*(1-t) + b*t        #interpolation
        
    def white_noise(self,dim,perm):
        """Génération d'un noise white, selon une graine (table de permutation)"""
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
    def ini(self,foyer=-1,firemans=-1):
        if(foyer < 0): foyer = int( np.ceil(self.size/30) )
        self.johny(foyer)               #allume le feu
        if(firemans < 0): firemans = int( np.ceil(self.size/3) )
        self.create_fireman(firemans)     #créer les firemans
        
    def turn(self):
        if(self.count == 0 and len(self.burn_list) < 1): self.ini()     #initialisation si cela n'a pas été fait
        self.count+= 1
        k = len(self.burn_list)
        i = 0
        while(i < k):
            if(len(self.burn_list) > 0):
                cell = self.search(self.burn_list[i].x,self.burn_list[i].y)        #on récupère la cellule qui va être propagé 
                cell.propagation(self)
                if(cell.charred == True): k -= 1      #si la cell vient d'être charrednisé, la size de burn_list a diminué
                i += 1
                
        display.draw(self,name='a')
        
        for frmn in self.fireman_list:
            frmn.update(self)
            if(frmn.hp <= 0): self.fireman_list.remove(frmn)         #le fireman est mort
            
        display.draw(self,name='b')
            
    
    def johny(self,n):
        """ ALLUMMEEEEEEEEEEEEEEEERR,  LE FEEUUU !! """
        for i in range(n):      #n: namebre de foyer de feu au début de la simulation
            b = True
            while(b):           #boucle de test pour ne pas bruler l'eau
                b = False
                x,y = rnd.randint(0,self.size-1),rnd.randint(0,self.size-1)
                cell = self.search(x,y)
                if(cell.nat == 0): b = True
            cell.state = 1
            self.burn_list.append(cell)
            
            
    def create_fireman(self,n):
        for i in range(n):      #n: namebre de firemans au début de la simulation
            name = "august"+str(i)
            b = True
            while(b):           #boucle de test pour ne pas mettre un fireman dans l'eau
                b = False
                x,y = rnd.randint(0,self.size-1),rnd.randint(0,self.size-1)
                cell = self.search(x,y)
                if(cell.nat == 0 or cell.state > 0): b = True
            self.fireman_list.append(frm.Fireman(name,x,y))     #créer un nouveau fireman et l'ajoute à la liste
        
        
    def search(self,x,y):
        """Cette fonction search une cell aux coordonnées x et y dans une liste d'objets Cell"""
        result = None
        for cell in self.cell_list:
            if(cell.x == x and cell.y == y): result = cell
        return result
        
    def calc_mat(self):
        """Cette fonction recalce la matrice self.map en fonction des cells dans la cell_list.
        Elle n'est normalement utilisé que pour l'displayfichage"""
        self.map = np.zeros([self.size,self.size])
        for cell in self.burn_list:       #on displayfecte d'abord les cells en feu
            i,j = cell.y,cell.x
            self.map[i,j] = 3 + cell.state
        
        for cell in self.cell_list:
            i,j = cell.y,cell.x
            if(self.map[i,j] == 0):       #si une valeur n'a pas déja été displayfecté
                    if(cell.charred == True):     #si c'est une cell charred, on lui displayfecte le maximum +1 (pour l'displayfichage)
                        self.map[i,j] = -1
                    else:
                        self.map[i,j] = cell.nat      #sinon, on displayfecte le chiffre correspondant à la nature
        
        
    def save(self):
        """Sauvegarde l'état actuel de la matrice"""
        db.save_map(self.cell_list,self.count)
        db.save_fireman(self.fireman_list,self.count)
        
    def construct(self,num):
        self.cell_list = []
        self.burn_list = []
        
        result = db.get_cell(num)
        for line in result:
            cell = cl.Cell(line[0],line[1],line[2],line[3],line[4])
            self.burn_list.append(cell)
            if(line[3] > 0 and line[4] == False):     #intensité > 0 et charred = Fasle
                self.burn_list.append(cell)
                
        self.fireman_list = []
        
        result = db.recup_fireman(num)
        for line in result:
            frmp = frm.Fireman(line[0],line[1],line[2],line[3])
            self.fireman_list.append(frmp)