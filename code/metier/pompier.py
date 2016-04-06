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


class Fireman(object):
    def __init__(self,name,x,y):
        self.name = str(name)     #le name sertd'identifiant
        self.x = x              #coordonnées
        self.y = y
        self.hp = 20
        
    def __str__(self):
        return "{}".format(self.name)
        
    def movement(self,other,n):
        """Déplacement d'un fireman vers une other cell"""
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
        
        
    def update(self,map):
        """Méthode principale du fireman, pour appeler les other fonctions"""
        own_cell = map.search(self.x,self.y)     #cell qui correspond à la position du fireman
        near = own_cell.get_near(map)               #list des cells nearacentes à squaree du fireman
        
        goal = self.search_fire(map.burn_list)        #search les cells qui burningnt
        if(goal != None):
            movement = True
            for cell in near:        #on search si le fireman est à coté du fire
                if(cell.x == goal.x and cell.y == goal.y): movement = False
                
            if(movement):
                self.go_to_fire(own_cell,near,goal)        #le fireman se déplace
            else:
                self.put_out_fire(own_cell,near,map)        #le fireman éteint le fire

        
    def search_fire(self,burn_list):
        """Cherche la cell qui burning la plus proche du fireman, selon la distance entre chaque cell qui burning"""
        dist = float('inf')
        cell = None
        
        for square in burn_list:        #parcourt la list des cells en fire
            temp = distance(self.x,self.y, square.x,square.y)
            if temp < dist:     #si la distance est plus courte, le fireman va choisir cette cell
                dist = temp
                cell = square
        return cell
            
            
    def go_to_fire(self,cell,list_near,cell_fire):
        """Gère le déplacement du fireman en fonction de sa position et de la position de la cell en fire"""
        if(cell.state > 0): self.hp -= cell.state                #le fireman est brulé d'un montant égal à l'intensité
        
        if(cell.state > 0 and cell.charred != True):       #si la cell du fireman est en fire, il s'en émap
            escape = cell
            for square in list_near:
                if square.state < escape.state:      #on search la cell à l'intensité la plus faible
                    escape = square
            self.movement(escape)             #déplacement en direction de l'escape
        
        else:
            move = True        #booléen pour savoir si fireman va mover ou non
            for square in list_near:
                if(cell_fire.x == square.x and cell_fire.y == square.y): move = False     #si la cell goal est nearacentes, le fireman ne se déplace pas
            
            if(move):
                if distance(self.x,self.y,cell_fire.x,cell_fire.y)>=4:
                    self.movement(cell_fire,2)     #déplacement en direction du fire en courant si on est loin
                else:
                    self.movement(cell_fire,1)     #déplacement en direction du fire en marchant si on est proche
                    
                    
    def put_out_fire(self,cell,list_near,map):
        """Calcul les cells nearacentes qui peuvent être éteintes à partir de la position actuelle du fireman"""
        burning = []      #list des squareules nearacentes qui burningnt
        for square in list_near:
            if(square.state > 0 and square.charred == False):      #si la cell burning, mais n'est pas cramé
                burning.append(square)
                
        if(len(burning) <= 3):        #si il y a moins de 3 cells en fire autour
            for square in burning:
                square.state -= 2              #on éteint la cell
                if(square.state < 0): square.state = 0  #l'intensité du fire n'est pas inférieure à 0
                if(square.state == 0): map.burn_list.remove(square)
                
        else:
            k=len(burning)
            i=0
            while i < k:
                r = rdm.randint(0,len(burning)-1)       #choix aléatoire de la cell à éteindre, parmis squarees disponibles
                square = burning[r]
                square.state -= 2
                if(square.state < 0): square.state = 0
                if(square.state == 0):
                    map.burn_list.remove(square)
                    burning.remove(burning[r])      #on retire la cell qui vient d'etre éteinte
                    
                i+=1
                k=len(burning)
