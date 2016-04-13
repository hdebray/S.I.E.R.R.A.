# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 11:49:48 2016

@author: ogustin
"""

import numpy as np
import random as rnd

import base.fireman as frm
import base.cell as cl
import db.data as db
from base.fireman import distance

    
class Map(object):
    def __init__(self,size):
        self.size = size                    #size of the map, the map is always a square
        self.map = np.zeros([size,size])    #init the matrix to display the map
        self.cell_list = []                 #list of the cell which compose the map
        self.burn_list = []                 #list of the cell which are actually burning
        self.fireman_list = []              #list of active firemen on the man
        self.count = 0                      #track the number of iterations
        
    """
    Create a map by combining 2 heightmap, randomly generated with a 'value noise'
    """
    def creation(self):
        """Combine two heightmap (height and moisture)"""
        height = self.heightmap()
        forest = self.heightmap()
        for i in range(self.size):
            for j in range(self.size):
                self.map[i,j] = self.biome(height,forest,i,j)        #create the map
        
                
    def biome(self,alti,forest,i,j):
        """Create the map by checking the height and moisture value of every cell"""
        n = 0
        if(alti[i,j] < 0.25):        #water
            n = 0
            self.cell_list.append(cl.Cell(j,i,0))
        elif(alti[i,j] > 0.6 and forest[i,j] > 0.5):     #forest
            n = 2
            self.cell_list.append(cl.Cell(j,i,2))
        elif(alti[i,j] > 0.6 and forest[i,j] < 0.3):     #town
            n = 3
            self.cell_list.append(cl.Cell(j,i,3))
        else:                       #grass
            n = 1
            self.cell_list.append(cl.Cell(j,i,1))
        return n
        
    def heightmap(self,amp=1,freq=1/2.0):
        """Create a heightmap by adding successive noise value, with differents amplitude and frequencies"""
        noise = np.zeros([self.size,self.size])     #initialisation
        while(self.size*freq > 1 and amp > 0.01):     #while the resolution is greater than 1
            noise += self.calc_noise(self.size*freq) * amp
            freq *= 0.4     #augment the frequency
            amp *= 0.6    #reduce the amplitude
        noise = self.distrib(noise)
        return noise
        
    def calc_noise(self,res):
        """Calcul a value for a certain resolution (size*freq)
        A new seed is generated for every noise"""
        perm = np.random.permutation(256)           #permutation table (world seed)
        self.white = self.white_noise(self.size,perm)                #white noise
        
        temp = np.zeros([self.size,self.size])
        for i in range(self.size):
            for j in range(self.size):
                temp[i][j] = self.smooth(i/res,j/res)      #interpolation to smooth the white noise
                
        return temp
        
    def smooth(self,y,x):
        """This function is smoothing the white noise, by using a bilinear interpolation 
        for a better result"""
        x0 = int(x)         #integer part
        frac_x = x - x0     #float part
        y0 = int(y)
        frac_y = y - y0
        
        x1 = (x0+1)
        y1 = (y0+1)
        if(x1 > len(self.white)-1): x1 = len(self.white)-1      #make sure the coord are below the max value
        if(y1 > len(self.white)-1): y1 = len(self.white)-1
        
        dx1 = self.lerp(frac_x,self.white[y0][x0],self.white[y0][x1])        #bilinear interpolation of the pixel's value
        dx2 = self.lerp(frac_x,self.white[y1][x0],self.white[y1][x1])
        result = self.lerp(frac_y,dx1,dx2)
        return result
        
    def lerp(self,p,a,b):
        """Interpolation of the value of point p, based on values of points a and b"""
        t = (p**2)*(3 - 2*p)            #cubic interpolation, better result than linear 
        return a*(1-t) + b*t            #interpolation
        
    def white_noise(self,dim,perm):
        """Generate a white noise, based on a permutation table"""
        mat = np.zeros([dim,dim])
        for i in range(dim):
            for j in range(dim):
                mat[i][j] = perm[ (j%256 + perm[i%256]) % 256 ]     #pseudo-random value
        return mat

    def distrib(self,mat):
        """Spread the values of a matrix in range [0,1]"""
        mx,mn = np.ceil(np.amax(mat)),np.floor(np.amin(mat))
        result = (mat-mn)/(mx-mn)
        return result
        
        
    """
    Update the simulation state
    """
    def ini(self,foyer=0,firemen=0):
        """Initialisation of the fire cells and the firemen"""
        if(foyer <= 0): foyer = int( np.ceil(self.size/50) )
        self.johnny(foyer)               #ingnite the fire
        if(firemen <= 0): firemen = int( np.ceil(self.size/3) )
        self.create_fireman(firemen)     #create the firemen
        
    def turn(self):
        """Calculate the simulation state on one iteration"""
        if(self.count == 0 and len(self.burn_list) < 1): self.ini()     #default init
        self.count+= 1
        
        k = len(self.burn_list)     #we store the length of burn_list, to only update the burned cells already existing
        i = 0
        while(i < k):
            if(len(self.burn_list) > 0):
                cell = self.search(self.burn_list[i].x,self.burn_list[i].y)        #store the cell to update
                cell.propagation(self)
                if(cell.charred == True): k -= 1      #if the cell is charred, reduce k
                i += 1
        
        txt = []            #list of textual informations
        for frmn in self.fireman_list:
            frmn.update(self)
            if(frmn.hp <= 0):
                self.fireman_list.remove(frmn)         #the fireman is dead
                txt.append(frmn.name+" est mort")
                
        return txt
                
        #display.draw(self,name='b',notif=txt)     #display the sim state after the firemen acted
            
    
    def johnny(self,n):
        """ ALLUMMEEEEEEEEEEEEEEEERR,  LE FEEUUU !! """
        for i in range(n):      #n: number of starting burning cell on initialisation
            b = True
            while(b):           #test loop to be sure water doesn't burn
                b = False
                x,y = rnd.randint(0,self.size-1),rnd.randint(0,self.size-1)
                cell = self.search(x,y)
                if(cell.nat == 0): b = True     #continue looping if it's water
            cell.state = 1
            self.burn_list.append(cell)
            
            
    def create_fireman(self,n):
        """Create n Fireman objects, and store them is fireman_list"""
        for i in range(n):      #n: number of starting firemen on initialisation
            name = "august"+str(i)      #one of them will be called 'august1'...
            b = True
            while(b):           #test loop to be sure fireman doesn't spawn in water
                b = False
                x,y = rnd.randint(0,self.size-1),rnd.randint(0,self.size-1)
                cell = self.search(x,y)
                if(cell.nat == 0 or cell.state > 0): b = True
            self.fireman_list.append(frm.Fireman(name,x,y))     #create a fireman and add it to fireman_list
        
        
    def search(self,x,y):
        """Search the Cell object with the right coordinates, and return this object"""
        result = None
        for cell in self.cell_list:
            if(cell.x == x and cell.y == y): result = cell
        return result
        
    def calc_mat(self):
        """Calculate the matrix's cells value based on their corresponding Cell object.
        Only used to display"""
        self.map = np.zeros([self.size,self.size])      #init
        for cell in self.burn_list:       #first set the burning cells
            i,j = cell.y,cell.x
            self.map[i,j] = 3 + cell.state      #value in range [4,8]
        
        for cell in self.cell_list:     #then the 'normal' cells
            i,j = cell.y,cell.x
            if(self.map[i,j] == 0):       #if it's not on fire, value will still be 0
                    if(cell.charred == True):
                        self.map[i,j] = -1      #Value -1 for destroyed cells
                    else:
                        self.map[i,j] = cell.nat      #Otherwise, value is equal to the nature (0 -> 3)
        
        
    def save(self):
        """Save the simulation state and the iterations count"""
        db.save_map(self.cell_list,self.fireman_list,self.count)
        
    def construct(self,num):
        """Recreate the simulation state, based on the cell_list and fire_man list, of the iteration 'n' """
        self.cell_list = []
        self.burn_list = []
        
        result = db.get_cell(num)       #collect every cells
        for line in result:
            cell = cl.Cell(line[0],line[1],line[2],line[3],line[4])
            self.cell_list.append(cell)
            if(line[3] > 0 and line[4] == False):     #intensity > 0 and charred = False
                self.burn_list.append(cell)
                
        self.fireman_list = []
        
        result = db.recup_fireman(num)  #collect every fireman
        for line in result:
            frmp = frm.Fireman(line[0],line[1],line[2],line[3])
            self.fireman_list.append(frmp)
            
    """
    Crée une liste de cases sur lesquelles les pompiers doivent aller
    """
#    def center(self):                               #cherche le barycentre des cases en feu
#        x_center=0
#        y_center=0
#        for cell in burn_list:
#            x_center+=self.burnlist[cell][0]/len(self.burn_list)
#            y_center+=self.burnlist[cell][1]/len(self.burn_list)
#            cent=[int(x_center),int(y_center)]
#        return cent
#            
#    def radius(self):                               #
#        centroide=self.center()
#        dist=0
#        for cell in self.burn_list:
#            dist=max(distance(centroide[0],centroide[1],cell.x,cell.y),dist)
#        return dist
#        
#    def wrapping(self):
#        wrap=[]
#        centroide=self.center()
#        rad=self.radius()
#        for cellmap in map.cell_list:
#            dist_cent=distance(centroide[0],centroide[1],cellmap.x,cellmap.y)
#            if dist_cent<=rad+0.5 and dist_cent>=rad-0.5:
#                wrap.append(cellmap)
#        return wrap
#        
#    def hemicycles(self,wrap):
#        hemi1=[]
#        hemi2=[]
#        for index in range(len(wrap)):
#            if index%2==1:
#                hemi1.append(wrap[index])
#            if index%2==0:
#                hemi2.append(wrap[index])
#        return hmccl1,hmccl2
#        
#    def cordon(self,burn_list,fireman_list):
#        frm_nber=len(fireman_list)
#        wrp=self.wrapping()
#        perimeter=len(wrp)
#        interval=int(perimeter/frm_nbr)
#        left_cordon,right_cordon=self.hemicycles(wrp)
#        cord=[]
#        cord.append(left_cordon[0])    
#        for leftcell in left_cordon:
#            if distance(leftcell.x,leftcell.y,left_cordon[-1].x,left_cordon[-1].y)>=interval:
#                cord.append(leftcell)
#        cord.append(right_cordon[0]) 
#        for rightcell in right_cordon:
#            if distance(rightcell.x,rightcell.y,right_cordon[-1].x,right_cordon[-1].y)>=interval:
#                cord.append(rightcell)
#        return cord       
#            