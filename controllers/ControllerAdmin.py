#!/usr/bin/python                                                                                                
# Admin Controller
# This model controls interactions with the indoor and outdoor weather actions which need to occur
import sys
import os

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

import cherrypy

class ControllerAdmin( object ):

  def __init__( self ):
    self.Renderer          = MVC.loadDriver('Renderer')
    self.Renderer.layout_h = 'admin/layout/header.html'
    self.Renderer.layout_f = 'admin/layout/footer.html'

  def index( self, **kwargs ):
    return self.Renderer.make( 'admin/login.html', header = False )
  index.exposed = True

  def auth( self, **kwargs ):
    if kwargs:
      print ''
    else:
      print ''
    return ''
  auth.exposed = True

  def dashboard( self ):
    return self.Renderer.make('admin/dashboard.html')    
  dashboard.exposed = True

  def users( self ):
    User = MVC.loadModel('User')
    data = {
      'users' : User.getAll()
    }
    return self.Renderer.make( 'admin/users/index.html', data = data )
  users.exposed = True

  def info( self, user_id = False ):
    User = MVC.loadModel( 'User' )
    data = {}
    if user_id != False:
      data['user'] = User.getById( user_id)
      return self.Renderer.make( 'admin/users/info.html', data )
    else:
      return 'error'
  info.exposed = True

  def create( self ):
    return self.Renderer.make( 'admin/users/create.html' )
  create.exposed = True

  def create_user_submit( self, **kwargs ):
    if kwargs:
      if kwargs['password_1'] == kwargs['password_2']:
        User = MVC.loadModel('User')
        new_user = User.create( kwargs['user_name'], kwargs['email'], kwargs['password_1'] )
        raise cherrypy.HTTPRedirect('/admin/users/') 
  create_user_submit.exposed = True

  def edit_user( self, **kwargs ):
    if kwargs:
      User = MVC.loadModel('User')
      User.update( kwargs['user_id'], kwargs['user_name'], kwargs['email'] )
      raise cherrypy.HTTPRedirect( '/admin/info/%s' % kwargs['user_id'] )
  edit_user.exposed = True

  def edit_password( self, **kwargs ):
    if kwargs:
      User = MVC.loadModel('User')
      if kwargs['password_1'] == kwargs['password_2']:
        User.updatePass( kwargs['user_id'], kwargs['password_1'] )
    raise cherrypy.HTTPRedirect( '/admin/info/%s' % kwargs['user_id'] )
  edit_password.exposed = True

  def delete_user( self, user_id = None ):
    if user_id:
      User = MVC.loadModel('User')
      User.delete( user_id )
      raise cherrypy.HTTPRedirect( '/admin/info/%s' % user_id )
  delete_user.exposed = True

  def create_user_meta( self, **kwargs ):
    if kwargs:
      User = MVC.loadModel('User')
      help_text = ''
      parent    = ''
      User.addMeta( kwargs['user_id'], kwargs['meta_key'], kwargs['meta_value'], kwargs['pretty_name'], help_text, parent )
      raise cherrypy.HTTPRedirect( '/admin/info/%s' % kwargs['user_id'] )
  create_user_meta.exposed = True

  def edit_user_meta( self, **kwargs ):
    if kwargs:
      User = MVC.loadModel('User')
      User.updateUserMeta( kwargs['user_id'], kwargs['meta_key'], kwargs['meta_value'], meta_id = kwargs['meta_id'] )
    raise cherrypy.HTTPRedirect( '/admin/info/%s' % kwargs['user_id'] )
  edit_user_meta.exposed = True

  def roles( self ):
    ACL = MVC.loadHelper('ACL')
    roles = ACL.getAllRoles()
    data = { 'roles': roles }
    return self.Renderer.make( 'admin/users/roles.html', data )
  roles.exposed = True
    
  def settings( self ):
    Settings = MVC.loadHelper('Settings')
    data = { 'options' : Settings.get_options() }
    return self.Renderer.make( 'admin/settings/index.html', data )
  settings.exposed = True

  def settings_update( self, **kwargs ):
    Settings = MVC.loadHelper( 'Settings')
    if kwargs['meta_id'] == '':
      Settings.create(  kwargs['meta_key'], kwargs['meta_value'] )
    else:
      Settings.update( kwargs['meta_key'], kwargs['meta_value'] )
    raise cherrypy.HTTPRedirect( '/admin/settings' )
  settings_update.exposed = True

  def settings_delete( self, meta_id ):
    Settings = MVC.loadHelper( 'Settings')
    Settings.delete( meta_id )
    raise cherrypy.HTTPRedirect( '/admin/settings' )
  settings_delete.exposed = True

# End File: controllers/ControllerAdmin.py
