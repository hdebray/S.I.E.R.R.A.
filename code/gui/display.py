# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 14:46:02 2016

@author: ogustin
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as col
import matplotlib.cm as cm
import PyQt4.QtGui as qtg
import PyQt4.QtCore as qtc

import base.map as mp

import warnings as war      #allow to filter warnings
import os

war.filterwarnings("ignore",category=RuntimeWarning)

#Create a discrete colormap, with hexa color codes
cpool = ['#2a0d03','#318fe5', '#51c353', '#4e8539', '#b6aba2', 
         '#dc6741', '#d44212', '#a9340e', '#7f270a', '#541a07']


def draw(map,svg=True,name='',hide=True,colorbar=False,notif=[]):
    """
    Display the map as 2D array, with a specific color for each Cell nature and state
    
    :param map: Map object which must be displayed
    :param svg: boolean, determine if the image must be saved or not
    :param name: string, add an additional name to 'imgXXX.png'
    :param hide: boolean, toggle the display of the drawn image
    :param colorbar: boolean, toggle the colorbar used at the right of the image
    :param notif: string array, contains every notification which must be displayed
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
        size = 3 + (frman_display[i][2])
        plt.plot(frman_display[i][0],frman_display[i][1],'rs',markersize=size)
    
    for i in range(len(notif)):                 #display the notifications
        plt.text(0,i*2, notif[i], color='w')
        
    wind_dir = ['N','NE','E','SE','S','SW','W','NW']  
    if(map.wind_active): plt.text(0,map.size,'wind: '+ wind_dir[map.wind], color='b')       #display wind notification
    
    plt.text(map.size/2, map.size, str(len(map.fireman_list)) + ' firemen alive', color='r')        #display number of firemen

    plt.axis([-0.5,map.size-0.5,-0.5,map.size-0.5])     #resize the image
    plt.axis('off')                                     #hide the axis
        
    if(svg):
        txt = "images/img" + str(map.count+100) + name + ".png"      #image's name, +100 for index problems (conversion)
        plt.savefig(txt,dpi=200,bbox_inches='tight',pad_inches=0)


def compile(delete=False):
    """
    Convert every png files in a single gif, with an option to delete after the conversion is done
    YOU SHALL HAVE Imagemagick INSTALLED TO CONVERT THE PNGs INTO A GIF !
        http://www.imagemagick.org/script/binary-releases.php
        
    :param delete: boolean, toggle the suppression of the images once the compilation is done
    """
    print('Compile result...')
    
    os.system('convert -delay 40 -loop 0 images/*.png images/simulation.gif')
    
    print("Done")
    
    if(delete): destroy()         #destroy the images
        
                
def destroy():
    """
    This function delete every images in the images/ directory
    """
    directory = 'images/'
    for file in os.listdir(directory):
        if(file[-3:] == 'png'):     #if the file have a 'png' extension
            path = directory+str(file)
            os.remove(path)         #remove the file
            
    print("Destroyed")
                
                
class Window(qtg.QWidget):
    """
    The Window class construct the main GUI window that is displayed on screen, it allow the user to change
    the simulation's options and see the result
    """
    def __init__(self):
        """The constructor."""
        super(Window, self).__init__()
        
        self.dim = int(qtg.QDesktopWidget().screenGeometry().height() / 2)  #max dimension of images
        self.set_wind = True
        self.initUI()
    
    def initUI(self):
        """
        Initiate the default interface with every buttons
        """
        grid = qtg.QGridLayout()            #grid layout to display options
        grid.setSpacing(20)
        
        #simulation size setting
        self.size_label = qtg.QLabel("Size:")        #label for anything
        self.size_label.setAlignment(qtc.Qt.AlignCenter)     #self-explicit...
        self.size = qtg.QSpinBox()
        self.size.setMinimum(1)
        self.size.setMaximum(300)
        self.size.setValue(50)
        self.size.setToolTip('Size of the map')        #info on hover
        self.size.valueChanged.connect(self.set_max)
        grid.addWidget(self.size_label, 0,0)
        grid.addWidget(self.size, 0,1)
        
        #number of fire on simulation start
        self.fire_label = qtg.QLabel("Fire:")
        self.fire_label.setAlignment(qtc.Qt.AlignCenter)
        self.fire = qtg.QSpinBox()
        self.fire.setMinimum(1)
        self.fire.setMaximum( int(np.ceil(self.size.value()/15)) )
        self.fire.setValue( int(np.ceil(self.size.value()/50)) )
        self.fire.setToolTip('Number of burning cell on start')
        self.fire.setDisabled(True)         #disable
        grid.addWidget(self.fire_label, 0,2)
        grid.addWidget(self.fire, 0,3)
        
        #number of firemen on simulation start
        self.frman_label = qtg.QLabel("Firemen:")
        self.frman_label.setAlignment(qtc.Qt.AlignCenter)  
        self.frman = qtg.QSpinBox()
        self.frman.setMinimum(1)
        self.frman.setMaximum( int(np.ceil(self.size.value()*2)) )
        self.frman.setValue( int(np.ceil(self.size.value()/3)) )
        self.frman.setToolTip('Number of firemen on start')
        self.frman.setDisabled(True)
        grid.addWidget(self.frman_label, 0,4)
        grid.addWidget(self.frman, 0,5)
        
        #toggle default settings
        self.default = qtg.QCheckBox("Default settings")
        self.default.toggle()
        self.default.stateChanged.connect(self.set_default)
        grid.addWidget(self.default, 1,0, 1,3)
        
        #toggle wind
        self.wind = qtg.QCheckBox("Wind")
        self.wind.setToolTip("Activate the wind for the simulation")
        self.wind.toggle()
        grid.addWidget(self.wind, 2,0, 1,3)
           
        #start the simulation
        self.start = qtg.QPushButton("START")
        self.start.setToolTip('Start the simulation')
        self.start.clicked.connect(self.solve)
        grid.addWidget(self.start, 1,6)
        
        #restart the simulation with same map as before
        self.restart = qtg.QCheckBox("Use same map")
        self.restart.setToolTip("Restart the simulation with the exact same map")
        self.restart.setDisabled(True)
        grid.addWidget(self.restart, 1,7, 1,3)
        
        #compile the images
        self.compile = qtg.QPushButton("Compile")
        self.compile.setDisabled(True)
        self.compile.setToolTip("Compile the result into a GIF \n"\
                                "/!\ You must have Imagemagick installed on your computer")
        self.compile.clicked.connect(compile)
        grid.addWidget(self.compile, 2,6)
        
        #add grid layout to main layout (vertical)
        main_layout = qtg.QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.addStretch(1)
        main_layout.addLayout(grid)
        
        #add logo image
        img_name = "gui/S.png"
        self.img_label = qtg.QLabel()
        self.img_label.setPixmap(qtg.QPixmap(img_name).scaled(self.dim,self.dim))
        self.img_label.setAlignment(qtc.Qt.AlignCenter)
        main_layout.addWidget(self.img_label)
        
        #set slider below image
        self.slider = qtg.QSlider(qtc.Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(0)
        self.slider.setTickPosition(qtg.QSlider.TicksBelow)
        main_layout.addWidget(self.slider)
        
        main_layout.addStretch(1)
        
        self.setLayout(main_layout)         #final touch
        self.resize(self.sizeHint())
        self.center()
        self.setWindowIcon(qtg.QIcon("gui/S.png"))
        self.setWindowTitle("S.I.E.R.R.A.")
        self.show()
        
        
    def center(self):
        """
        This function center the window in the centr of the screen
        """
        rect = self.frameGeometry()         #size of widget
        center = qtg.QDesktopWidget().availableGeometry().center()      #center of screen resolution
        rect.moveCenter(center)     #move center point of rect to center point of screen
        self.move(rect.topLeft())     #move widget to top left corner of rect
        
    def set_default(self):
        """
        Activate and calculate the default values for fire and firemen numbers
        """
        if(self.default.isChecked()):
            self.fire.setDisabled(True)
            self.fire.setValue(int(np.ceil(self.size.value()/50)))
            self.frman.setDisabled(True)
            self.frman.setValue(int(np.ceil(self.size.value()/3)))
        else:
            self.fire.setDisabled(False)
            self.frman.setDisabled(False)
            
    def set_max(self):
        """
        Change the max value and the value allowed to fire and firemen when the map size change
        """
        self.fire.setMaximum( int(self.size.value()/15) )
        self.frman.setMaximum( int(self.size.value()*2) )
        if(self.default.isChecked()):
            self.frman.setValue( int(np.ceil(self.size.value()/3)) )
            self.fire.setValue( int(np.ceil(self.size.value()/50)) )
        if(self.fire.value == 0): self.fire.setValue(1)
            
    def set_slider(self, value):
        """
        Configure the slider when the simulation is finished
        
        :param value: integer, set the max value of the slider
        """
        self.slider.setMinimum(0)
        self.slider.setMaximum(value)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.change_img)
        self.img_label.setPixmap(qtg.QPixmap("images/img100.png").scaled(self.dim,self.dim,aspectRatioMode=qtc.Qt.KeepAspectRatio))
        
    def change_img(self):
        """
        Change the displayed image based on the value of the slider
        """
        value = self.slider.value()
        img_name = "images/img"+str(value+100)+".png"
        self.img_label.setPixmap(qtg.QPixmap(img_name).scaled(self.dim,self.dim,aspectRatioMode=qtc.Qt.KeepAspectRatio))
        
        
    def solve(self):
        """
        Main functionnality of the app: solve the simulation with the input parameters
        print() function are for debugging purpose only
        """
        self.start.setDisabled(True)        #disable start button while calculating
        self.compile.setDisabled(True)
        
        print('Initialisation...')
        destroy()
        map = mp.Map(self.size.value())
        map.creation()
        map.ini(self.fire.value(),self.frman.value(),self.wind.isChecked(),self.restart.isChecked())
        
        draw(map)
        
        print('Calculating...')
        i=0
        while(len(map.burn_list) > 0 and len(map.fireman_list) > 0):        #main simulation loop
            text = map.turn()
            draw(map,notif=text)
            
            i+=1
            if(i>5*map.size):break      #seatbelt, to prevent accidents
        
        self.set_slider(i)      #configure the slider
        
        print('Complete !')
        self.start.setDisabled(False)
        self.compile.setDisabled(False)
        self.restart.setDisabled(False)
        