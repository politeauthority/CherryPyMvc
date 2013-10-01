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
    view = env.get_template('base/index.html')
    return view.render( d = {} )
  index.exposed = True



  def admin( self ):
    view = env.get_template('base/admin/login.html')
    return view.render( d = {} )
  admin.exposed = True

  def dashboard( self ):
    view = env.get_template('base/admin/dashboard.html')
    return view.render( d = {} )
  dashboard.exposed = True

  def users( self ):
    User = MVC.loadModel('User')
    data = {
      'users' : User.getAll()
    }
    print data
    view = env.get_template('base/admin/users/index.html')
    return view.render( d = data )
  users.exposed = True

  def info( self, user_id = False ):
    User = MVC.loadModel( 'User' )
    data = {}
    if user_id != False:
      data['user'] = User.getById( user_id)
      print user_id
      print data
      view = env.get_template('base/admin/users/info.html')
      return view.render( d = data )
    else:
      return 'error'
  info.exposed = True

  def create( self ):
    view = env.get_template('base/admin/users/create.html')
    return view.render( d = {} )
  create.exposed = True

  def create_user_submit( self, **kwargs ):
    if kwargs:
      if kwargs['password_1'] == kwargs['password_2']:
        User = MVC.loadModel('User')
        new_user = User.create( kwargs['user_name'], kwargs['email'], kwargs['password_1'] )
        return new_user
  create_user_submit.exposed = True

  def roles( self ):
    ACL = MVC.loadHelper('ACL')
    roles = ACL.getAllRoles()
    data = { 'roles': roles }
    view = env.get_template('base/admin/users/roles.html')    
    return view.render( d = data )
  roles.exposed = True
    
  def settings( self ):
    view = env.get_template('base/admin/settings/index.html')
    return view.render( d = {} )
  settings.exposed = True

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

root            = Root()
root.admin      = Root().admin()
root.dashboard  = Root().dashboard()
root.users      = Root().users()
root.info       = Root().info()
root.create     = Root().create()
root.create_user_submit = Root().create_user_submit()
root.roles      = Root().roles()
root.settings   = Root().settings()


cherrypy.quickstart(  Root(),  config = MVC.cherrypy_config )

# End File: server.py