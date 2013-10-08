#!/usr/bin/python                                                                                                
# Main Web Server application file  
# 

import sys
import os

from MVC import MVC
MVC = MVC()
# End file header                                                               

from sys import path
import cherrypy

Root = MVC.loadController( 'Home', callable = True )

cherrypy.quickstart( Root(),  config = MVC.cherrypy_config )

# End File: server.py
