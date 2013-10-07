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

  # @todo: make this work!
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
    ACL  = MVC.loadHelper( 'ACL' )
    data = {}
    if user_id != False:
      data['user']  = User.getById( user_id )
      data['roles'] = ACL.getAllRoles()
      return self.Renderer.make( 'admin/users/info.html', data )
    else:
      return 'error'
  info.exposed = True

  # should be absolved into self.users as a modal window
  def create( self ):
    return self.Renderer.make( 'admin/users/create.html' )
  create.exposed = True

  def user_add( self, **kwargs ):
    if kwargs:
      if kwargs['password_1'] == kwargs['password_2']:
        User = MVC.loadModel('User')
        new_user = User.create( kwargs['user_name'], kwargs['email'], kwargs['password_1'] )
        raise cherrypy.HTTPRedirect('/admin/users/') 
  user_add.exposed = True

  def user_edit( self, **kwargs ):
    if kwargs:
      User = MVC.loadModel('User')
      User.update( kwargs['user_id'], kwargs['user_name'], kwargs['email'] )
      raise cherrypy.HTTPRedirect( '/admin/info/%s' % kwargs['user_id'] )
  user_edit.exposed = True

  def user_password_edit( self, **kwargs ):
    if kwargs:
      User = MVC.loadModel('User')
      if kwargs['password_1'] == kwargs['password_2']:
        User.updatePass( kwargs['user_id'], kwargs['password_1'] )
    raise cherrypy.HTTPRedirect( '/admin/info/%s' % kwargs['user_id'] )
  user_password_edit.exposed = True

  def user_perms_edit( self, **kwargs ):
    if kwargs:
      ACL = MVC.loadHelper( 'ACL' )
      try:
        role_ids = kwargs['acl_roles']
      except:
        role_ids = []
      ACL.updateUserRoles( kwargs['user_id'], role_ids )

      try:
        perm_ids = kwargs['acl_perms']
      except:
        perm_ids = []

      return str( perm_ids )
      ACL.updateUserPerms( kwargs['user_id'], perm_ids )
    raise cherrypy.HTTPRedirect( '/admin/info/%s' % kwargs['user_id'] )
  user_perms_edit.exposed = True

  def user_delete( self, user_id = None ):
    if user_id:
      User = MVC.loadModel('User')
      User.delete( user_id )
      raise cherrypy.HTTPRedirect( '/admin/info/%s' % user_id )
  user_delete.exposed = True

  # should be user_meta_create // OR combined with edit_user_meta
  def create_user_meta( self, **kwargs ):
    if kwargs:
      User = MVC.loadModel('User')
      help_text = ''
      parent    = ''
      User.addMeta( kwargs['user_id'], kwargs['meta_key'], kwargs['meta_value'], kwargs['pretty_name'], help_text, parent )
      raise cherrypy.HTTPRedirect( '/admin/info/%s' % kwargs['user_id'] )
  create_user_meta.exposed = True

  def user_meta_edit( self, **kwargs ):
    if kwargs:
      User = MVC.loadModel('User')
      User.updateUserMeta( kwargs['user_id'], kwargs['meta_key'], kwargs['meta_value'], meta_id = kwargs['meta_id'] )
    raise cherrypy.HTTPRedirect( '/admin/info/%s' % kwargs['user_id'] )
  user_meta_edit.exposed = True

  def user_acl( self ):
    ACL = MVC.loadHelper('ACL')
    roles = ACL.getAllRoles()
    data = { 'roles': roles }
    return self.Renderer.make( 'admin/users/acl.html', data )
  user_acl.exposed = True
  
  # Updates a Role
  def user_acl_role_update( self, **kwargs ):
    if kwargs:
      ACL = MVC.loadHelper( 'ACL' )
      if kwargs['role_id'] == '':
        ACL.createRole( kwargs['role_name'] )
    raise cherrypy.HTTPRedirect( '/admin/user_acl/' )
  user_acl_role_update.exposed =  True

  # Updates a Permission
  # should be user_acl_perm_update
  def acl_perm_update( self, **kwargs ):
    if kwargs:
      ACL = MVC.loadHelper( 'ACL' )
      if kwargs['perm_id'] == '':
        Misc = MVC.loadHelper( 'Misc' )
        perm_id = ACL.createPerm( Misc.slug( kwargs['perm_name'] ), kwargs['perm_name'] )[0]
        if kwargs['role_id'] != '':
          ACL.createRolePerm( kwargs['role_id'], perm_id )
      raise cherrypy.HTTPRedirect( '/admin/user_acl/' )
  acl_perm_update.exposed =  True  

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
