# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 11:49:48 2016

@author: ogustin
"""

import numpy as np
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
class Map(object):
    def __init__(self,size):
        self.size = size
        
    def terraform(self):
        """Combine deux heightmap, puis construit la carte qui en dépend"""
        earth = np.zeros([self.size,self.size])
        height = self.heightmap()
        forest = self.heightmap()
        for i in range(self.size):
            for j in range(self.size):
                earth[i,j] = self.biome(height,forest,i,j)
        return earth
                
    def biome(self,height,forest,i,j):
        """Construit la carte en combinant les valeurs des deux heightmap"""
        value = 0
        if(height[i,j] < 0.4): value = 0        #eau
        elif(height[i,j] > 0.6 and forest[i,j] > 0.5): value = 2        #foret
        elif(height[i,j] > 0.7 and forest[i,j] < 0.4): value = 3        #ville
        else: value = 1         #plaine
        return value
                
        
    def heightmap(self,scale=1,freq=1/2.0):
        """Construit une heightmap en ajoutant successivement des bruits de valeurs,
        à des amplitudes et des fréquences différentes"""
        noise = np.zeros([self.size,self.size])     #initialisation
        while(self.size*freq > 1 and scale > 0.01):     #tant que la résolution de la carte est supérieur à 1
            noise += self.calc_noise(self.size*freq) * scale
            freq *= 0.4     #augmentation de la fréquence
            scale *= 0.6    #diminution de l'amplitude
        noise = self.norm(noise)
        return noise
        
    def calc_noise(self,res):
        """Calcul un bruit de valeur pour une résolution données (taille*fréquence).
        La graine utilisé pour générer le bruit blanc de départ est différente à chaque fois"""
        seed = np.random.permutation(256)           #table de permutation aléatoire (graine du monde)
        self.white = self.white_noise(self.size,seed)                #bruit blanc
        temp = self.interpol(res)         #interpolation du bruit blanc en fonction de la résolution
        return temp
        
    def interpol(self,res):
        """Interpolation du bruit blanc pour générer le bruit de valeur"""
        result = np.zeros([self.size,self.size])
        for i in range(self.size):
            for j in range(self.size):
                m,n = int(i/res),int(j/res)
                result[i][j] = self.smooth(i/res,j/res)
        return result
        
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
        t = (p**2)*(3 - 2*p)          #lissage de l'interpolation, cubique 
        return a*(1-t) + b*t        #interpolation
        
    def white_noise(self,size,seed):
        """Génération d'un bruit blanc, selon une graine (table de permutation)"""
        mat = np.zeros([size,size])
        for i in range(size):
            for j in range(size):
                mat[i][j] = seed[ (j%256 + seed[i%256]) % 256 ]
        return mat

    def norm(self,mat):
        """Redistribue les valeurs d'une matrice entre 0 et 1"""
        mx,mn = np.ceil(np.amax(mat)),np.floor(np.amin(mat))
        result = (mat-mn)/(mx-mn)
        return result

    def adjust(self,mat,value):
        """Cette fonction permet d'augmenter ou de diminuer la valeur globale d'une matrice,
        toujours entre 0 et 1"""
        if(value < 0.01): value = 1
        mat = mat**value
        return mat


mappy = Map(20)     #initialise une carte (ne pas dépasser une taille de 1000, sinon calcul trop long)
map1 = mappy.terraform()        #calcul de la carte, utilisable pour la simulation

height = mappy.heightmap()      #exemple d'une carte de hauteur

plt.matshow(map1,cmap=sim_color)

#plt.colorbar()         #affiche la carte de couleurs utilisé sur le graphique
#plt.savefig("map.png",dpi=250,facecolor='white')           #sauvegarde en tant qu'image