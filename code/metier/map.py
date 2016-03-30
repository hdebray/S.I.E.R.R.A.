# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 11:49:48 2016

@author: ogustin
"""

import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import matplotlib.colors as col
import matplotlib.cm as cm

"""
Création d'une carte de couleur continue linéaire, à partir d'une série de valeurs RGB
"""
color_map = { 'red': ((0.0, 0.007, 0.007),
                      (0.25, 0.035, 0.035),
                      (0.49, 0.067, 0.067),
                      (0.5, 0.271, 0.271),
                      (0.51, 0.165, 0.165),
                      (0.75, 0.451, 0.451),
                      (0.85, 0.6, 0.6),
                      (0.95, 0.7, 0.7),
                      (1.0, 1.0, 1.0)),
            'green': ((0.0, 0.168, 0.168),
                      (0.25, 0.243, 0.243),
                      (0.49, 0.322, 0.322),
                      (0.5, 0.424, 0.424),
                      (0.51, 0.4, 0.4),
                      (0.75, 0.5, 0.5),
                      (0.85, 0.561, 0.561),
                      (0.95, 0.702, 0.702),
                      (1.0, 1.0, 1.0)),
             'blue': ((0.0, 0.267, 0.267),
                      (0.25, 0.361, 0.361),
                      (0.49, 0.439, 0.439),
                      (0.5, 0.463, 0.463),
                      (0.51, 0.161, 0.161),
                      (0.75, 0.302, 0.302),
                      (0.85, 0.361, 0.361),
                      (0.95, 0.702, 0.702),
                      (1.0, 1.0, 1.0))}
                      
earth_color = col.LinearSegmentedColormap('earth',color_map,N=256)

"""
Création d'une carte de couleurs finies par valeurs discrètes, en code hexadécimal
"""
cpool = ['#0085ff', '#00e503', '#4e8539', '#cbbeb5', '#2a0d03',
         '#d85429', '#d44212', '#be3b10', '#a9340e', '#942e0c']
sim_color = col.ListedColormap(cpool[0:4], 'indexed')
cm.register_cmap(cmap=sim_color)
    


"""
Création d'une carte en combinant deux cartes de hauteur (heightmap), 
générées par un bruit de valeur (Value Noise)
"""
class Carte(object):
    def __init__(self,taille):
        self.taille = taille
        self.carte = np.zeros([taille,taille])
        self.liste_case = []
        self.liste_brule = []
        self.liste_pompier = []
        self.iter = 0
        
    def creation(self,foyer=-1):
        """Combine deux heightmap (altitude et humidité), puis construit la carte qui en dépend"""
        alti = self.heightmap()
        foret = self.heightmap()
        for i in range(self.taille):
            for j in range(self.taille):
                self.carte[i,j] = self.biome(alti,foret,i,j)        #créé la carte
        
        
        if(foyer < 0): foyer = int(self.taille/10)
        self.johny(foyer)
        self.creer_pomp(n)
                
    def biome(self,alti,foret,i,j):
        """Construit la carte en combinant les valeurs des deux heightmap"""
        n = 0
        if(alti[i,j] < 0.4):        #eau
            n = 0
            #self.liste_case.append(Case(j,i,0))
        elif(alti[i,j] > 0.6 and foret[i,j] > 0.5):     #foret
            n = 2
            #self.liste_case.append(Case(j,i,2))
        elif(alti[i,j] > 0.7 and foret[i,j] < 0.4):     #maison
            n = 3
            #self.liste_case.append(Case(j,i,3))
        else:               #plaine
            n = 1
            #self.liste_case.append(Case(j,i,1))
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
    def tour(self,*pompiers):
        self.iter+= 1
    
    def johny(self,n):
        """ ALLUMMEEEEEEEEEEEEEEEERR,  LE FEEUUU !! """
        for i in range(n):
            b = True
            while(b):           #boucle de test pour ne pas bruler l'eau
                b = False
                a,b = rnd.randint(0,self.taille-1)
                case = self.cherche(a,b)
                if(case.nat != 0): b = True
            case.etat = 1
            self.liste_brule.append(case)
            
    def creer_pomp(self,n):
        for i in range(n):
            nom = "august"+str(i)
            a,b = rnd.randint(0,self.taille-1)
            #liste_pompier.append(Pompier(nom,a,b))     #créer un nouveau pompier et l'ajoute à la liste
        
    def cherche(self,x,y):
        """Cette fonction cherche une case aux coordonnées x et y, et renvoie l'objet Case correspondant"""
        result = None
        for case in self.liste_case:
            if(case.x == x and case.y == y): result = case
        return result
        
#    def sauvegarde(self):
#        bd.sauve_carte(self.liste_case,self.tour)
        
        


carte = Carte(50)     #initialise une carte (ne pas dépasser une taille de 1000, sinon calcul trop long)

#alti = carte.heightmap()      #exemple d'une carte de hauteur
carte.creation()        #calcul de la carte, utilisable pour la simulation

plt.matshow(carte,cmap=sim_color)

plt.colorbar()         #affiche la carte de couleurs utilisé sur le graphique
#plt.savefig("map.png",dpi=250,facecolor='white')           #sauvegarde en tant qu'image