# -*- coding: utf-8 -*-

'''
Created on Mar 28, 2014

@author: jaime
'''


class Login(object):

    def __init__(self, username, password, project, authurl):
        self._username = username
        self._password = password
        self._project = project
        self._authurl = authurl
        
    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, username):
        self._username = username
    
    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, passwd):
        self._password = passwd
    
    @property    
    def project(self):
        return self._project
    
    @project.setter
    def project(self, project):
        self._project = project
        
    @property
    def authurl(self):
        return self._authurl
    
    @authurl.setter
    def authurl(self, authurl):
        self._authurl = authurl