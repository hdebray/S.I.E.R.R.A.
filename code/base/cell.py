# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 09:53:14 2016

@author: Henri
"""

import random as rdm
import numpy as np

"""
Convention: water=0; grass=1; forest=2; town=3
"""

wind0=np.array([[2, 1.5, 1],
               [1.5, 0, .5],
               [1, .5, 0]])
               
wind1=np.array([[1.5, 1, .5],
               [2, 0, 0],
               [1.5, 1, .5]])

wind2=np.array([[1, .5, 0],
               [1.5, 0, .5],
               [2, 1.5, 1]])
               
wind3=np.array([[1.5, 2, 1.5],
               [1, 0, 1],
               [.5, 0, .5]])
               
wind4=np.array([[.5, 0, .5],
               [1.5, 0, .5],
               [1.5, 2, 1.5]])

wind5=np.array([[1, 1.5, 2],
               [.5, 0, 1.5],
               [0, .5, 1]])
               
wind6=np.array([[.5, 1, 1.5],
               [0, 0, 2],
               [.5, 1, 1.5]])
               
wind7=np.array([[0, .5, 1],
               [.5, 0, 1.5],
               [1, 1.5, 2]])


class Cell(object):
    def __init__(self,x,y,nat,state=0,charred=False):
        self.x = x
        self.y = y
        self.nat = nat      #nature of the cell (see 'convention' above)
        self.state = state      #intensity of the fire on the cell
        self.charred = charred      #boolean to test if cell is destroyed
        
    def __str__(self):
        if(self.nat == 0): txt = 'water'
        if(self.nat == 1): txt = 'grass'
        if(self.nat == 2): txt = 'forest'
        if(self.nat == 3): txt = 'town'
        return "{} (x:{},y:{})".format(txt,self.x,self.y)
            
    def get_near(self,map):
        """Utilisty function to get the list of cells near the "self" cell"""
        near_cells = []
        for i in range(self.x-1, self.x+2):
            for j in range(self.y-1, self.y+2):
                if(i>=0 and i<map.size and j>=0 and j<map.size): near_cells.append(map.search(i,j))
        return near_cells
        
        
    
    def propagation(self,map):
        """This function calculate the growing intensity of burning cells, and spread the fire around them"""
        near_cells = self.get_near(map)
        
        #fire spreading
        burnable = []                  #list of burnable cells
        for cell in near_cells:
            if(cell.nat != 0 and cell.state == 0):  #conditions to burn a cell
                burnable.append(cell)
                
        if(self.nat == 2):                          #spread faster if it's a forest
            n = rdm.randint(0,(self.state*2))        #n: number of cells to burn, n < 9
            if n>8: n=8
        else: n = rdm.randint(0,self.state)
        
        if n>=len(burnable):               #if n is greater than the number of burnable cells, they are all burned
            for cell in burnable:
                cell.state = 1
                map.burn_list.append(cell)      #add cell to burn_list
        else:                
            for i in range(n):
                
                #creating the list in which the choice is made (changing probability according to the wind direction)
                indexes=[]
                for ce in burnable:
                    
                    indexes.append(near_cells.index(ce))
                    
                    if map.wind==0:
                        if ce.y <= self.y:
                            indexes.append(near_cells.index(ce))    #*2 probability if the cells in direction of fire
                        if ce.y >= self.y:
                            indexes.remove(near_cells.index(ce))    #0 probability if cell against the fire
                        
                    if map.wind==4:
                        if ce.y >= self.y:
                            indexes.append(near_cells.index(ce))    #*2 probability if the cells in direction of fire
                        if ce.y <= self.y:
                            indexes.remove(near_cells.index(ce))    #0 probability if cell against the fire
                    
                    if map.wind==2:
                        if ce.x >= self.x:
                            indexes.append(near_cells.index(ce))    #*2 probability if the cells in direction of fire
                        if ce.x <= self.x:
                            indexes.remove(near_cells.index(ce))    #0 probability if cell against the fire
                            
                    if map.wind==6:
                        if ce.x <= self.x:
                            indexes.append(near_cells.index(ce))    #*2 probability if the cells in direction of fire
                        if ce.x >= self.x:
                            indexes.remove(near_cells.index(ce))    #0 probability if cell against the fire
                            
                    
                
                r = rdm.choice(indexes)   #choose randoly the cell, among the availables
                cell = near_cells[r]
                cell.state = 1                       #cell is burned
                map.burn_list.append(cell)
                burnable.remove(cell)      #the cell is no more available
                
        #fire intensity growing       
        if(self.nat == 3):  #burn faster if it's a house
            self.state += 2
        else:
            self.state += 1
            
        if(self.state > 5):      #if it's burned
            self.charred = True
            self.state = 1
            map.burn_list.remove(self)      #burned cells are removed form the burn_list
            