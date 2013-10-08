#!/usr/bin/python                                                                                                
# AdminUser Controller
# This Controller handles Admin - User based interactions
import sys
import os

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header

import cherrypy

class ControllerAdminUser( object ):

  def __init__( self ):
	self.Renderer          = MVC.loadDriver('Renderer')
	self.Renderer.layout_h = 'admin/layout/header.html'
	self.Renderer.layout_f = 'admin/layout/footer.html'

  def index( self  ):
	User = MVC.loadModel('User')
	data = {
	  'users' : User.getAll()
	}
	return self.Renderer.make( 'admin/user/index.html', data = data )
  index.exposed = True

  def info( self, user_id = False ):
	UserModel = MVC.loadModel( 'User' )
	ACL       = MVC.loadHelper( 'ACL' )
	# user = UserModel.getById( user_id )
	data = {}
	if user_id != False:
	  data['user']  = UserModel.getById( user_id )
	  data['roles'] = ACL.getAllRoles()
	  return self.Renderer.make( 'admin/user/info.html', data )
	else:
	  return 'error'
  info.exposed = True

  def edit( self, **kwargs ):
	if kwargs:
	  User = MVC.loadModel('User')
	  User.update( kwargs['user_id'], kwargs['user_name'], kwargs['email'] )
	  raise cherrypy.HTTPRedirect( '/admin/user/info/%s' % kwargs['user_id'] )
  edit.exposed = True

  def password_edit( self, **kwargs ):
	if kwargs:
	  User = MVC.loadModel('User')
	  if kwargs['password_1'] == kwargs['password_2']:
		User.updatePass( kwargs['user_id'], kwargs['password_1'] )
	raise cherrypy.HTTPRedirect( '/admin/user/info/%s' % kwargs['user_id'] )
  password_edit.exposed = True

  def perms_edit( self, **kwargs ):
	if kwargs:
	  ACL = MVC.loadHelper( 'ACL' )
	  try:
		role_ids = kwargs['acl_roles[]']        
	  except:
		role_ids = []
	  try:
		perm_ids = kwargs['acl_perms[]']
	  except:
		perm_ids = []
	  ACL.updateUserAccess( kwargs['user_id'], role_ids, perm_ids )
	raise cherrypy.HTTPRedirect( '/admin/user/info/%s' % kwargs['user_id'] )
  perms_edit.exposed = True

  def meta_create( self, **kwargs ):
	if kwargs:
	  User = MVC.loadModel('User')
	  help_text = ''
	  parent    = ''
	  User.addMeta( kwargs['user_id'], kwargs['meta_key'], kwargs['meta_value'], kwargs['pretty_name'], help_text, parent )
	  raise cherrypy.HTTPRedirect( '/admin/user/info/%s' % kwargs['user_id'] )
  meta_create.exposed = True

  def meta_edit( self, **kwargs ):
	if kwargs:
	  User = MVC.loadModel('User')
	  User.updateUserMeta( kwargs['user_id'], kwargs['meta_key'], kwargs['meta_value'], meta_id = kwargs['meta_id'] )
	raise cherrypy.HTTPRedirect( '/admin/user/info/%s' % kwargs['user_id'] )
  meta_edit.exposed = True

  # should be absolved into self.users as a modal window
  def create( self ):
	return self.Renderer.make( 'admin/user/create.html' )
  create.exposed = True

  def add( self, **kwargs ):
	if kwargs:
	  if kwargs['password_1'] == kwargs['password_2']:
		User = MVC.loadModel('User')
		new_user = User.create( kwargs['user_name'], kwargs['email'], kwargs['password_1'] )
		raise cherrypy.HTTPRedirect('/admin/user/') 
  add.exposed = True

  def delete( self, user_id = None ):
	if user_id:
	  User = MVC.loadModel('User')
	  User.delete( user_id )
	  raise cherrypy.HTTPRedirect( '/admin/user/info/%s' % user_id )
  delete.exposed = True

  ### ACL Maintenence Feaures ###

  def acl( self ):
    ACL = MVC.loadHelper('ACL')
    roles = ACL.getAllRoles()
    data = { 'roles': roles }
    return self.Renderer.make( 'admin/user/acl.html', data )
  acl.exposed = True
  
  # Updates a Rolels
  def acl_role_update( self, **kwargs ):
    if kwargs:
      ACL = MVC.loadHelper( 'ACL' )
      if kwargs['role_id'] == '':
        ACL.createRole( kwargs['role_name'] )
    raise cherrypy.HTTPRedirect( '/admin/user_acl/' )
  acl_role_update.exposed =  True

  # Updates a Permission
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

# End File: controllers/admin/ControllerAdminUser.py