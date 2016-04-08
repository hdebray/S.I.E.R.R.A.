# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 14:46:02 2016

@author: ogustin
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as col
import matplotlib.cm as cm

import warnings as war      #allow to filter warnings
import os

war.filterwarnings("ignore",category=RuntimeWarning)

"""
Create a linear colormap, with RGB values
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
Create a discrete colormap, with hexa color codes
"""
cpool = ['#2a0d03','#318fe5', '#51c353', '#4e8539', '#b6aba2', 
         '#dc6741', '#d44212', '#a9340e', '#7f270a', '#541a07']


def draw(map,svg=True,name='',hide=True,colorbar=False,text=[]):
    """Display the map with the matrix of values.
    svg to save the image, name for specific name, hide to hide the image, colorbar to show the colorbar
    """
    map.calc_mat()      #update the matrix
    mx = int( np.amax(map.map) )      #max and min values of the matrix
    mn = int( np.amin(map.map) )      #to determine the colormap used
    
    
    simu_color = col.ListedColormap(cpool[(mn+1):(mx+2)], 'indexed')
    cm.register_cmap(cmap=simu_color)
    color = simu_color
        
    if(hide): plt.ioff()         #hide the poping windows of python
    else: plt.ion()
    
    if(colorbar): plt.colorbar()     #show the colormap used to draw the matrix
    
    
    #list of displayed fireman on the map, to draw bigger symbols when there is multiple firemen on same cell
    frman_display = []
    for frman in map.fireman_list:
        new = True
        for i in range(len(frman_display)):
            if(frman.x == frman_display[i][0] and frman.y == frman_display[i][1]):       #if there is already a fireman on this position
                new = False
                break
        if(not new): frman_display[i][2] += 1       #size of the symbol whill be bigger
        else: frman_display.append([frman.x,frman.y,0])     #new position to draw a symbol
                
                
    
    plt.matshow(map.map,cmap=color)     #display the map
    
    
    for i in range(len(frman_display)):          #display firemen with a red square
        size = 3 + (frman_display[i][2] * 2)
        plt.plot(frman_display[i][0],frman_display[i][1],'rs',markersize=size)
    
    for i in range(len(text)):
        plt.text(0,i, text[i], color='w')
        
        
    plt.axis([-0.5,map.size-0.5,-0.5,map.size-0.5])     #resize the image
    plt.axis('off')                                     #hide the axis
        
    if(svg):
        txt = "images/img" + str(map.count+100) + name + ".png"      #image's name, +100 for index problems (conversion)
        plt.savefig(txt,dpi=100,bbox_inches='tight',pad_inches=0)


def compile(delete=False):
    """Convert every png files in a single gif, with an option to delete after the conversion is done
    YOU SHALL HAVE Imagemagick INSTALLED TO CONVERT THE PNGs INTO A GIF !
    """
    
    os.system('convert -delay 40 -loop 0 images/*.png images/simulation.gif')
    
    if(delete):    # destroy the images
        directory = 'images/'
        for file in os.listdir(directory):
            if(file[-3:] == 'png'):     #if the file have a 'png' extension
                path = directory+str(file)
                os.remove(path)         #remove it
    
    