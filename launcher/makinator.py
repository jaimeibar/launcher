# -*- coding: utf-8 -*-
# $Id$
# Description
# Author: jim

# Distributed under GNU/GPL 2 license

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/



'''
Created on Mar 25, 2014

@author: jaime
'''


from novaclient.client import Client
from novaclient.exceptions import Unauthorized, NotFound
from getpass import getpass
import sys



class Login(object):

    def __init__(self, **kwargs):
        self._password = kwargs.get("password", "")
        self._username = kwargs.get("username", "")
        self._project = kwargs.get("project", "")
        self._authurl = kwargs.get("authurl", "")
        
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


def get_password():
    passwd = getpass().strip()
    return passwd

def do_openstack_login(data):
    try:
        nova = Client(2, data.username, data.password, data.project, data.authurl)
        nova.authenticate()
        return nova
    except Unauthorized, e:
        print >> sys.stderr, "Login error: {0}".format(e.message)
        sys.exit(1)
    except e:
        print >> sys.stderr, "Error: {0}".format(e.message)
        sys.exit(1)

def get_flavour_list(data, name=""):
    if not name:
        print "Flavors available"
        for i, flavor in enumerate(data.flavors.list()):
            print "{0} - Id: {1} ---- Name: {2}".format(i, flavor.id, flavor.name)
    else:
        try:
            return data.flavors.find(name=name)
        except NotFound:
            print >> sys.stderr, "Flavour {0} not found".format(name)
            sys.exit(1)

def get_image_name(data, name=""):
    if not name:
        print "Images availables"
        for i, image in enumerate(data.images.list()):
            print "{0} - Id: {1} ---- Name: {2}".format(i, image.id, image.name)
    else:
        try:
            return data.images.find(name=name)
        except NotFound:
            print >> sys.stderr, "Image {0} not found".format(name)
            sys.exit(1)

def get_security_group(data, name="default"):
    try:
        return data.security_groups.find(name=name)
    except NotFound:
        print >> sys.stderr, "Security group {0} not found".format(name)
        print "Security groups"
        for i, group in enumerate(data.security_groups.list()):
            print "{0} - Id: {1} ---- Name: {2}".format(i, group.id, group.name)
        sys.exit(1)            

def get_keypairs(data, name=""):
    if not name:
        print "Keypairs"
        for i, key in enumerate(data.keypairs.list()):
            print "{0} - Id: {1} ---- Name: {2}".format(i, key.id, key.name)
    else:
        try:
            return data.keypairs.find(name=name)
        except NotFound:
            print >> sys.stderr, "Key {0} not found".format(name)
            sys.exit(1)

def launch_virtual_machines(data, name, image, flavour, **kwargs):
    secgroups = kwargs.get("secgroup", None)
    secgroups.name if kwargs.get("secgroup") else None
    kpair = kwargs.get("kpair", None)
    images = data.servers.create(name, image, flavour, 
                                 security_groups=[secgroups.name], 
                                 key_name=kpair.name)
    return images

def main():
    passw = get_password()
    logininfo = Login(password=passw)
    nova = do_openstack_login(logininfo)
    image = get_image_name(nova, "CirrOS 0.3.1")
    flavour = get_flavour_list(nova, "m1.tiny")
    secgroup = get_security_group(nova)
    keypair = get_keypairs(nova)
    if not any([image, flavour]):
        print >> sys.stderr, "Not enough parameters"
        sys.exit(1)
    imgs = launch_virtual_machines(nova, "test", image, flavour, 
                                   secgroup=secgroup, kpair=keypair)
    return 0


if __name__ == '__main__':
    sys.exit(main())