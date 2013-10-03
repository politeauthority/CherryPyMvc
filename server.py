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

class Root( object ):
  
  admin = MVC.loadController('Admin')

  def __init__( self ):  
    self.Renderer          = MVC.loadDriver('Renderer')
    #self.Renderer.layout_h = 'admin/layout/header.html'
    #self.Renderer.layout_f = 'admin/layout/footer.html'

  def index( self ):
    return self.Renderer.make('base/index.html')
  index.exposed = True

  def dashboard( self ):
    return self.Renderer.make( 'base/admin/dashboard.html' )
  dashboard.exposed = True

  def error_page_404( status, message, traceback, version ):
    Renderer = MVC.loadDriver('Renderer')
    return Renderer.make( 'errors/404.html', header = False )
  cherrypy.config.update({'error_page.404': error_page_404})  

cherrypy.quickstart( Root(),  config = MVC.cherrypy_config )

# End File: server.py