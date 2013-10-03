#!/usr/bin/python
# Installer
# This will have to be run as root, as we will be installing all our dependancies here                                   
import sys
import os

sys.path.append( os.path.join(os.path.dirname(__file__), '..', '') )
from MVC import MVC
MVC = MVC()
# End file header
import subprocess

#install our python dependancies
subprocess.call( "apt-get install python-cherrypy3", shell=True )
subprocess.call( "apt-get install python-jinja2",   shell=True )
subprocess.call( "apt-get install python-bs4",   shell=True )
Mysql = MVC.loadDriver('Mysql')
Mysql.ex( 'CREATE DATABASE IF NOT EXISTS `%s`;' % MVC.db['name'] )

# Base Website tables                                                                                                                                         
createTable_options = """CREATE TABLE `"""+ MVC.db['name'] +"""`.`options` (                                                                                  
  `id`              int(9) NOT NULL AUTO_INCREMENT,                                                                                       
  `meta_key`        varchar(200) NOT NULL,                                                                                                                
  `meta_value`      varchar(200) NOT NULL,                                                                                                                        
  `parent`          int(10) DEFAULT 0,                                                                                                                            
  `pretty_name`     varchar(250) DEFAULT NULL,                                                                                                                    
  `help_text`       varchar(250) DEFAULT NULL,                                                                                                                    
  PRIMARY KEY (`id`)                                                                                                                                          
); """

# User tables                                                                                                                                                 
createTable_users  = """CREATE TABLE `"""+ MVC.db['name'] +"""`.`users` (                                                                                     
  `id`              int(9)       NOT NULL AUTO_INCREMENT,                                                                                 
  `user`            varchar(100) NOT NULL,                                                                                                
  `email`           varchar(250) NOT NULL,                                                                                                        
  `pass`            varchar(250) NOT NULL,                                                                                                
  `last_login`      varchar(15) DEFAULT NULL,                                                                                                                     
  PRIMARY KEY (`id`)                                                                                                                                          
);"""

createTable_usermeta = """CREATE TABLE `"""+ MVC.db['name'] +"""`.`usermeta` (                                                                                
  `id`              int(9) NOT NULL AUTO_INCREMENT,                                                                                       
  `user_id`         int(10) NOT NULL,                                                                                                                     
  `parent`          int(10) NOT NULL,                                                                                                             
  `meta_key`        varchar(200) NOT NULL,                                                                                                                
  `meta_value`      varchar(200) NOT NULL,                                                                                                                        
  `pretty_name`     varchar(250) DEFAULT NULL,                                                                                                                    
  `help_text`       varchar(250) DEFAULT NULL,                                                                                                            
  PRIMARY KEY (`id`)                                                                                                                                          
); """

createTable_user_acl_roles       = """CREATE TABLE `"""+ MVC.db['name'] +"""`.`acl_roles` (                                                                   
  `id`             int(10) unsigned NOT NULL AUTO_INCREMENT,                                                                                     
  `roleName`       varchar(20) NOT NULL,                                                                                                                         
  PRIMARY KEY (`ID`),                                                                                                                                         
  UNIQUE KEY `roleName` (`roleName`)                                                                                                                          
); """

createTable_user_acl_user_perms  = """CREATE TABLE `"""+ MVC.db['name'] +"""`.`acl_user_perms` (                                                              
  `id`              bigint(20) unsigned NOT NULL AUTO_INCREMENT,                                                                                      
  `userID`          bigint(20) NOT NULL,                                                                                                                      
  `permID`          bigint(20) NOT NULL,                                                                                                                      
  `value`           tinyint(1) NOT NULL DEFAULT '0',                                                                                                          
  `addDate` datetime NOT NULL,                                                                                                                                
  PRIMARY KEY (`ID`),                                                                                                                                         
  UNIQUE KEY `userID` (`userID`,`permID`)                                                                                                                     
 ); """

createTable_user_acl_user_roles  = """CREATE TABLE `"""+ MVC.db['name'] +"""`.`acl_user_roles` (                                                              
  `userID`          bigint(20) NOT NULL,                                                                                                                          
  `roleID`          bigint(20) NOT NULL,                                                                                                                          
  `addDate`         datetime NOT NULL,                                                                                                                            
  UNIQUE KEY `userID` (`userID`,`roleID`)                                                                                                                     
); """


Mysql.ex( createTable_options )
Mysql.ex( createTable_users )
Mysql.ex( createTable_usermeta )
Mysql.ex( createTable_user_acl_roles )
Mysql.ex( createTable_user_acl_user_perms )
Mysql.ex( createTable_user_acl_user_roles )









# End File install/install.py