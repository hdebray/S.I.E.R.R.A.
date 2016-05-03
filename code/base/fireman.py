# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 15:20:49 2016
@author: Amaury
"""
import numpy as np
import random as rdm

def distance(x1,y1,x2,y2):  
    """
    Returns the euclidian distance between points 1 and 2
    
    :param x1: integer
    :param y1: integer
    :param x2: integer
    :param y2: integer
    :return: the distance between the points (x1,y1) and (x2,y2)
    
    Tests
    ---
    >>>distance(0,0,0,0)
    0
    
    >>>distance(0,1,0,0)
    1
    
    >>>distance(0,0,1,1) == np.sqrt(2)
    True
    """
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)



class Fireman(object):
    """
    The Fireman class describes the firemen. They are defined by their name, their coodinates,
    and their health points.
    """
    def __init__(self,name,x,y,hp=20.):
        """The constructor.
        
        :param name: string
        :param x: integer, first coordinate
        :param y: integer, second coordinate
        :param hp: float, health points
        
        
        Tests
        ---
        >>>Fireman('john')
        Traceback (most recent call last):
            ...
        TypeError: __init__() missing 2 required positional arguments: 'x' and 'y'
        
        """
        self.name = str(name)     #the name is equal to an id
        self.x = x
        self.y = y
        self.hp = hp        #number of hit points. if hp = 0, the fireman dies
        
    def __str__(self):
        """The display: displays the firman's name"""
        return "{}".format(self.name)
        
    def movement(self,other,n=1):
        """Movement of the fireman to an other cell, by n step(s)
        
        :param other: cell
        :param n: integer
        """
        if self.x < other.x and self.y < other.y:
            self.x,self.y = self.x+n,self.y+n
        elif self.x < other.x and self.y > other.y:
            self.x,self.y = self.x+n,self.y-n
        elif self.x > other.x and self.y > other.y:
            self.x,self.y = self.x-n,self.y-n
        elif self.x > other.x and self.y < other.y:
            self.x,self.y = self.x-n,self.y+n
        elif self.x > other.x and self.y == other.y:
            self.x = self.x-n
        elif self.x < other.x and self.y == other.y:
            self.x = self.x+n
        elif self.x == other.x and self.y > other.y:
            self.y = self.y-n
        elif self.x == other.x and self.y < other.y:
            self.y = self.y+n
            
    def check_bounds(self,maximum):
        """Make sure that the fireman can't go outside the map
        
        :param maximum: integer (size of the map)
        """
        if(self.x < 0): self.x = 0
        if(self.x > maximum): self.x = maximum
        if(self.y < 0): self.y = 0
        if(self.y > maximum): self.y = maximum
        
    def update(self,map):
        """Main function of the fireman, to call other functions
        
        :param map: map        
        """
        own_cell = map.search(self.x,self.y)     #cell corresponding to fireman's position
        near = own_cell.get_near(map)               #cells near the fireman
        
        goal = self.search_fire(map.burn_list)        #search the burning cells
        if(goal != None):
            self.go_to_fire(own_cell,near,goal)         #fireman move
            self.check_bounds(map.size-1)               #and stay in the grid
            self.put_out_fire(own_cell,near,map)        #fireman put out the fire

        
    def search_fire(self,burn_list):
        """Search the closest burning cell, based on the fireman's distance with every burning cells
        
        :param burn_list: list of cells
        :return: the nearest burning cell
        """
        dist = float('inf')
        cell = None
        
        for square in burn_list:
            temp = distance(self.x,self.y, square.x,square.y)
            if temp < dist:     #if the distance is shorter, the fireman will choose that cell
                dist = temp
                cell = square
        return cell
            
            
    def go_to_fire(self,cell,list_near,cell_fire):
        """Manage the movement of the fireman, based on his own position and his objective
        
        :param cell: cell of the fireman
        :param list_near: list of neighboring cells
        :param cell_fire: list of burning cells
        """
        if(cell.state > 0):        #fireman burned by the intensity of the fire
            if(cell.charred == True):
                self.hp -= 0.5          #charred cell only burn by half of the intensity
            else:
                self.hp -= cell.state
        
        if(cell.state > 0 and cell.charred != True):       #escape the the fire, to not get hurt
            escape = cell
            for square in list_near:
                if square.state < escape.state:      #search the near cell with the lowest intensity
                    escape = square
            self.movement(escape)             #move to the escape
        
        else:
            move = True        #boolean to check if the fireman can move
            for square in list_near:
                if(cell_fire.x == square.x and cell_fire.y == square.y): move = False     #fireman doesn't need to move if his goal is near
            
            if(move):
                if(cell.nat == 0):                 #move slowly in water
                    self.movement(cell_fire,1)
                elif distance(self.x,self.y,cell_fire.x,cell_fire.y)>=4:
                    self.movement(cell_fire,2)     #run to the fire if it's far
                else:
                    self.movement(cell_fire,1)     #otherwise, move slowly
                    
                    
    def put_out_fire(self,cell,list_near,map):
        """Calculate the near cells  where the fire must disappear
        
        :param cell: cell of the fireman
        :param list_near: lit of neighboring cells
        :param map: map
        """
        burning = []      #list of burning cells near the fireman
        for square in list_near:
            if(square.state > 0 and square.charred == False):      #if it's burning, but not charred yet
                burning.append(square)
                
        if(len(burning) <= 3):        #if there is less than 3 burning cells
            for square in burning:
                square.state -= 2              #put out the fire
                if(square.state < 0): square.state = 0       #intensity can't go below 0
                if(square.state == 0): map.burn_list.remove(square)     #remove the cell from the burn_list
                
        else:
            k=len(burning)
            i=0
            while i < k:
                r = rdm.randint(0,len(burning)-1)       #randomly choose the cell, among the availables
                square = burning[r]
                square.state -= 2
                if(square.state < 0): square.state = 0
                if(square.state == 0):
                    map.burn_list.remove(square)        #remove the cell from burn_list if it's no more on fire
                    burning.remove(burning[r])          #cell no more available
                    
                i+=1
                k=len(burning)
