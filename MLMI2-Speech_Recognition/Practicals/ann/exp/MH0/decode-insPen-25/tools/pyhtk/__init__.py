#!/usr/bin/env python3
# coding=utf-8
# ----------------------------------------------------------- #
#                                                             #
#                          ___                                #
#                       |_| | |_/    HTK AUTOMATIC SPEECH     #
#                       | | | | \    RECOGNITION SOFTWARE     #
#                       =========    PYTHON SCRIPT INTERFACE  #
#                                                             #
#                                                             #
# ----------------------------------------------------------- #
# developed at:                                               #
#                                                             #
#           Machine Intelligence Laboratory                   #
#           Department of Engineering                         #
#           University of Cambridge                           #
#           http://mi.eng.cam.ac.uk/                          #
#                                                             #
# author:                                                     #
#           Chao Zhang <cz277@cam.ac.uk>                      #
#                                                             #
# ----------------------------------------------------------- #
#           Copyright: Cambridge University                   #
#                      Engineering Department                 #
#            2015-2016 Cambridge, Cambridgeshire UK           #
#                      http://www.eng.cam.ac.uk               #
#                                                             #
#   Use of this software is governed by a License Agreement   #
#    ** See the file License for the Conditions of Use  **    #
#    **     This banner notice must not be removed      **    #
#                                                             #
# ----------------------------------------------------------- #
# __init__.py: htklib root directory init file                #
# ----------------------------------------------------------- #

#import htklib.basic
#import htklib.model
#import htklib.inout
#from . import basic
#from . import model
#from . import inout
from .basic import *
from .model import *
from .data import *
from .inout import *
from .babel import *
from .method import *
 
# set all enabled modules of this package
#__all__ = ['basic', 'inout', 'model']

#import htklib.basic

#__all__ = ['basic']

#print('hello parent')


