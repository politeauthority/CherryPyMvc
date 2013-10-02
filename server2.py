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

Renderer          = MVC.loadDriver('Renderer')
Renderer.layout_h = 'admin/layout/header.html'
Renderer.layout_f = 'admin/layout/footer.html'

class Root:
    
  def index( self ):
    return Renderer.make( 'admin/frontpage.html' )
  index.exposed = True

  def error_page_404(status, message, traceback, version):
    return Renderer.make( 'errors/404.html', header = False )
  cherrypy.config.update({'error_page.404': error_page_404})

  def auth( user_name, password ):
    sql = 'SELECT * FROM %s.users WHERE `user` = "%s" AND `pass` = MD5( "%s" )' % ( user_name, password )
    auth = Mysql.ex( sql )
    if auth:
      return self.getById( auth[0] )
    else:
      return False

root            = Root()


cherrypy.quickstart(  Root(),  config = MVC.cherrypy_config )

# End File: server.py
