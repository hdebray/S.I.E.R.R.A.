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

class Cell(object):
    """Cell class
    The cells are the components of the map, they have a position defined by their coodinates
    x and y, their nature (water=0; grass=1; forest=2; town=3), their burning state (from 0 to 5),
    and if they are charred or not (using a boolean).
    """
    def __init__(self,x,y,nat,state=0,charred=False):
        """The constructor.
        
        :param x: integer
        :param y: integer coordinates
        :param nat: integer in [0,3], nature of the cell, following the convention
        :param state: integer in [0,5], burning state of the cell
        :param charred: boolean, True if the cell is charred
        """
        self.x = x
        self.y = y
        self.nat = nat      #nature of the cell (see 'convention' above)
        self.state = state      #intensity of the fire on the cell
        self.charred = charred      #boolean to test if cell is destroyed
        
    def __str__(self):
        """The display: displays the nature and the position"""
        if(self.nat == 0): txt = 'water'
        if(self.nat == 1): txt = 'grass'
        if(self.nat == 2): txt = 'forest'
        if(self.nat == 3): txt = 'town'
        return "{} (x:{},y:{})".format(txt,self.x,self.y)
            
    def get_near(self,map):
        """Utility function to get the list of cells near the "self" cell
        
        :param map: map
        :return list of the near cells
        """
        near_cells = []
        for i in range(self.x-1, self.x+2):
            for j in range(self.y-1, self.y+2):
                if(i>=0 and i<map.size and j>=0 and j<map.size): near_cells.append(map.search(i,j))
        return near_cells
        
        
    
    def propagation(self,mape):
        """This function calculates the growing intensity of burning cells, and spreads the fire around them
        
        :param map: map
        """
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
        
        if map.wind_active:                
            for i in range(n):
                
                #creating the list in which the choice is made (changing probability according to the wind direction)
                indexes=[]
                for ce in burnable:
                                        
                    if map.wind==0:
                        if ce.y > self.y:
                            indexes.append(near_cells.index(ce))    #*2 probability if the cells in direction of fire
                            indexes.append(near_cells.index(ce))
                        elif ce.y == self.y:
                            indexes.append(near_cells.index(ce))    #0 probability if cell against the fire
                                                                    #1 for the rest
                    elif map.wind==4:
                        if ce.y < self.y:
                            indexes.append(near_cells.index(ce))    #*2 probability if the cells in direction of fire
                            indexes.append(near_cells.index(ce))
                        elif ce.y== self.y:                 
                            indexes.append(near_cells.index(ce))    #0 probability if cell against the fire
                                                                    #1 for the rest
                    elif map.wind==2:
                        if ce.x > self.x:
                            indexes.append(near_cells.index(ce))    #*2 probability if the cells in direction of fire
                            indexes.append(near_cells.index(ce))
                        elif ce.x == self.x:
                            indexes.append(near_cells.index(ce))    #0 probability if cell against the fire
                                                                    #1 for the rest
                    elif map.wind==6:
                        if ce.x < self.x:
                            indexes.append(near_cells.index(ce))    #*2 probability if the cells in direction of fire
                            indexes.append(near_cells.index(ce))
                        elif ce.x == self.x:
                            indexes.append(near_cells.index(ce))    #0 probability if cell against the fire
                                                                    #1 for the rest                          
                    elif map.wind==1:
                        if ce.y >= self.y and ce.x >= self.x:
                            indexes.append(near_cells.index(ce))    #*2 probability if the cells in direction of fire
                            indexes.append(near_cells.index(ce))
                        elif (ce.y > self.y and ce.x < self.x) or (ce.y < self.y and ce.x > self.x):
                            indexes.append(near_cells.index(ce))                            

                    elif map.wind==3:
                        if ce.y <= self.y and ce.x >= self.x:
                            indexes.append(near_cells.index(ce))    #*2 probability if the cells in direction of fire
                            indexes.append(near_cells.index(ce))
                        elif (ce.y > self.y and ce.x > self.x) or (ce.y < self.y and ce.x < self.x):
                            indexes.append(near_cells.index(ce))      
                            
                    elif map.wind==5:
                        if ce.y <= self.y and ce.x <= self.x:
                            indexes.append(near_cells.index(ce))    #*2 probability if the cells in direction of fire
                            indexes.append(near_cells.index(ce))
                        elif (ce.y > self.y and ce.x < self.x) or (ce.y < self.y and ce.x > self.x):
                            indexes.append(near_cells.index(ce))
                            
                    elif map.wind==7:
                        if ce.y >= self.y and ce.x <= self.x:
                            indexes.append(near_cells.index(ce))    #*2 probability if the cells in direction of fire
                            indexes.append(near_cells.index(ce))
                        elif (ce.y > self.y and ce.x > self.x) or (ce.y < self.y and ce.x < self.x):
                            indexes.append(near_cells.index(ce))
                            
                
                if len(indexes)>0:
                    r = rdm.choice(indexes)   #choose randoly the cell, among the availables, with weight
                    cell = near_cells[r]
                    cell.state = 1                       #cell is burned
                    map.burn_list.append(cell)
                    burnable.remove(cell)      #the cell is no more available
        




        #without the wind active
        else:
            if n>=len(burnable):               #if n is greater than the number of burnable cells, they are all burned
                for cell in burnable:
                    cell.state = 1
                    map.burn_list.append(cell)      #add cell to burn_list
            else:                
                for i in range(n):
                    r = rdm.randint(0,len(burnable)-1)   #choose randoly the cell, among the availables
                    cell = burnable[r]
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
            
    def in_fire(self):
        """This function returns a boolean determining if the cell is on fire"""
        Fire=False
        if self.state>0 and self.state<=5:
            Fire=True
        return Fire
            
            
