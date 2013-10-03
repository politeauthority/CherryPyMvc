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

env = Environment( loader=FileSystemLoader('views') )

class Admin( object ):

  def index( self ):
    view = env.get_template('base/admin/login.html')
    return view.render( d = {} )
  index.exposed = True

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
      print ''
      print ''
      print ''
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

  def edit_user( self, **kwargs ):
    if kwargs:
      User = MVC.loadModel('User')
      User.update( kwargs['user_id'], kwargs['user_name'], kwargs['email'] )
    return 'need redirect'
  edit_user.exposed = True

  def edit_password( self, **kwargs ):
    if kwargs:
      User = MVC.loadModel('User')
      if kwargs['password_1'] == kwargs['password_2']:
        User.updatePass( kwargs['user_id'], kwargs['password_1'] )
    return 'needs redirect'
  edit_password.exposed = True

  def delete_user( self, user_id = None ):
    if user_id:
      User = MVC.loadModel('User')
      User.delete( user_id )
      return 'deleted'
  delete_user.exposed = True

  def create_user_meta( self, **kwargs ):
    if kwargs:
      User = MVC.loadModel('User')
      help_text = ''
      parent    = ''
      User.addMeta( kwargs['user_id'], kwargs['meta_key'], kwargs['meta_value'], kwargs['pretty_name'], help_text, parent )
      return 'success'
  create_user_meta.exposed = True

  def edit_user_meta( self, **kwargs ):
    if kwargs:
      User = MVC.loadModel('User')
      User.updateUserMeta( kwargs['user_id'], kwargs['meta_key'], kwargs['meta_value'], meta_id = kwargs['meta_id'] )
      return 'success'
  edit_user_meta.exposed = True

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

class Root( object ):
  
  admin = Admin()

  def index( self ):
    view = env.get_template('base/index.html')
    return view.render( d = {} )
  index.exposed = True

  def dashboard( self ):
    view = env.get_template('base/admin/dashboard.html')
    return view.render( d = {} )
  dashboard.exposed = True

cherrypy.quickstart(  Root(),  config = MVC.cherrypy_config )

# End File: server.py