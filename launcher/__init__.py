from launcher.makinator import do_openstack_login, get_flavour_list
from launcher.makinator import get_image_name, get_security_group
from launcher.makinator import get_keypairs, launch_virtual_machines

__all__ = ['do_openstack_login', 'get_flavour_list', 'get_image_name',
           'get_security_group', 'get_keypairs', 'launch_virtual_machines']
__version__ = '0.1'
