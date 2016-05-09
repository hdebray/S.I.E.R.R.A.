# -*- coding: utf-8 -*-
"""
Created on Mon May 09 16:48:05 2016

@author: Amaury
"""

import doctest

import base.map as mp
import base.cell as cl
import base.fireman as frm
import gui.display as disp
import db.data as db


if __name__=='__main__': 
    doctest.testmod(mp)
    doctest.testmod(cl)
    doctest.testmod(frm)
    doctest.testmod(disp)
    doctest.testmod(db)   