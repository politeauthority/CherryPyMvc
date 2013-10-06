#!/usr/bin/python
# Model View Controller Class
# A relativly simple class to help connect and unify the Garden Pi web and hardware aspects

import sys
from sys import path
import os

from config.webserver_config import settings as cherrypy_config
from config.app_config import settings as app_config

class MVC( object ):

  def __init__( self ):
    self.app_name     = 'Framework 1'
    self.app_dir      = os.path.abspath( os.path.dirname(__file__) ) + '/'
    self.logging      = True
    self.raspberry_pi = True
    self.db           = {
      'host' : app_config['database']['host'],
      'name' : app_config['database']['name'],
      'user' : app_config['database']['user'],
      'pass' : app_config['database']['pass'],
    }

    self.cherrypy_config = cherrypy_config
    #self.cherrypy_config['global']['server.sock_port'] = garden_pi_config['webserver']['host_port']
    #self.cherrypy_config['global']['server.sock_host'] = garden_pi_config['webserver']['host_ip']
    #self.cherrypy_config['/']['tools.staticdir.root']  = '%spublic_html' % self.app_dir

  def loadDriver( self, driver_name ):
    return self.__load( 'Driver', driver_name )

  def loadController( self, controller_name ):
    return self.__load( 'Controller', controller_name )

  def loadModel( self, model_name ):
    return self.__load( 'Model', model_name )

  def loadHelper( self, helper_name ):
    return self.__load( 'Helper', helper_name )

  def __load( self, type, name ):
    path.insert( 1, self.app_dir + type.lower() + 's')
    item_name = type + name
    __import__( item_name )
    item = getattr( sys.modules[ "%s" % item_name ], "%s" % item_name )()
    return item

# Endfile: MVC.py
