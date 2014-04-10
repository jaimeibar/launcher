# -*- coding: utf-8 -*-

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
import sys



def do_openstack_login(data):
    try:
        nova = Client(2, data.username, data.password, data.project, data.authurl)
        nova.authenticate()
        return nova
    except Unauthorized, e:
        print >> sys.stderr, "Login error: {0}".format(e.message)
        sys.exit(1)
    except Exception, e:
        print >> sys.stderr, 'Unknown error. {0}'.format(e.message)
        sys.exit(1)

def get_flavour_list(data, name=""):
    if not name:
        print "Flavors available"
        for i, flavor in enumerate(data.flavors.list()):
            print '{0}\nId: {1}\nName: {2}\nDisk: {3}\nPublic: {4}\nRam: {5}\nVcpus: {6}'.format(i, flavor.id, flavor.name,
                                                                                                 flavor.disk, flavor.is_public,
                                                                                                 flavor.ram, flavor.vcpus)
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
            print "{0}\nId: {1}\nName: {2}\nStatus: {3}".format(i, image.id,
                                                                image.name,
                                                                image.status)
    else:
        try:
            return data.images.find(name=name)
        except NotFound:
            print >> sys.stderr, "Image {0} not found".format(name)
            sys.exit(1)

def get_security_group(data, name=""):
    if not name:
        print "Security Groups"
        for i, group in enumerate(data.security_groups.list()):
            print "{0} - Id: {1} ---- Name: {2}".format(i, group.id, group.name)
    else:
        try:
            return data.security_groups.find(name=name)
        except NotFound:
            print >> sys.stderr, "Security group {0} not found".format(name)
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
    secgroups = kwargs.get("secgroup")
    kpair = kwargs.get("kpair")
    instances = kwargs.get('instances')
    images = data.servers.create(name, image, flavour, max_count=instances,
                                 security_groups=[secgroups],
                                 key_name=kpair)
    return images
