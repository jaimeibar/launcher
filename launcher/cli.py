# -*- coding: utf-8 -*-

import sys
import argparse
import getpass
from launcher.login import Login
from launcher.makinator import do_openstack_login



def _parse_arguments():
    parser = argparse.ArgumentParser(description="Launch virtual machines to OpenStack")

    parser.add_argument('-u', '--user', action='store', required=True, 
                        dest='username', help='The username for login')
    parser.add_argument('-p', '--password', action='store_true', required=True,
                        dest='password', 
                        help='The password will be prompted after run the program')
    parser.add_argument('--url', action='store', required=True, dest='url',
                        help='The authentication url')
    parser.add_argument('--tenant', action='store', required=True, dest='tenant',
                        help="The tenant name")

    image_group = parser.add_argument_group('Image options')
    igexclusive = image_group.add_mutually_exclusive_group(required=True)
    igexclusive.add_argument('-i', '--image', action='store', dest='image', 
                       help="Image name to launch")
    igexclusive.add_argument('-l', '--list', action='store', dest='list', 
                       help='List all images availables')

    flavour_group = parser.add_argument_group('Flavour options')
    fgexclusive = flavour_group.add_mutually_exclusive_group(required=True)
    fgexclusive.add_argument('--flavour', help='Flavour to use')
    fgexclusive.add_argument('--flist', help='List all available flavours')

    return parser.parse_args()


def main():
    arguments = _parse_arguments()
    user = arguments.username
    pwd = getpass.getpass().strip()
    if not pwd:
        print >> sys.stderr, 'Error: No password provided'
        return 1
    url = arguments.url
    tenant = arguments.tenant
    logininfo = Login(user, pwd, url, tenant)
    return 0
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