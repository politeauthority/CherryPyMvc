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
from jinja2 import Environment, FileSystemLoader

path.insert( 1, 'config')
from webserver_config import settings

env = Environment( loader=FileSystemLoader('views') )

class Root:
    
  def index( self ):
    return view.render( d = {} )
  index.exposed = True

  #Example exposed method
  #def weather( self ):
  #  Weather = MVC.loadModel('Weather')
  #  tpl_args = {
  #    'weather_current' : Weather.get_current(),
  #    'weather_min_max' : Weather.get_min_max(),
  #  }
  #  view = env.get_template('weather/index.html')
  #  return view.render( d = tpl_args )
  #weather.exposed = True

root = Root()
#root.weather          = Root().weather()

cherrypy.quickstart(  Root(),  config = MVC.cherrypy_config )

# End File: server.py
