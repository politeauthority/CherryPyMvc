#!/usr/bin/python                                                   
# Renderer Driver 
# This driver helps build an html page 
# 

import sys
import os

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

from jinja2 import Environment, FileSystemLoader

class DriverRenderer( object ):

  def __init__( self ):
    self.layout_h = ''
    self.layout_f = ''
    self.env = env = Environment( loader=FileSystemLoader( MVC.app_dir + 'views') )

  def make( self, view, data = None, header = None, footer = None ):
    html_source = ''
    if self.layout_h != '':
      if header != False:
        html_source = self.draw( self.layout_h, header )
    
    html_source = html_source + self.draw( view, data )

    if self.layout_f != '' or header == False:
      if header != False:
        html_source = html_source + self.draw( self.layout_f, footer )

    return html_source
      
  def draw( self, view, data = None ):
    view = self.env.get_template( view )
    return view.render( d = data )
    
# End File: driver/DriverRenderer.py
