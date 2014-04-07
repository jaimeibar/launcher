# -*- coding: utf-8 -*-


import sys
import argparse
import getpass
import os
from launcher.login import Login
from launcher.urlchecker import UrlChecker
from launcher.makinator import do_openstack_login, get_image_name
from launcher.makinator import get_flavour_list



def _parse_arguments():
    parser = argparse.ArgumentParser(description="Launch virtual machines to OpenStack")

    parser.add_argument('-u', '--user', action='store', dest='username', 
                        help='The username for login. Defaults to env[LAUNCHER_USER].')
    parser.add_argument('-p', '--password', action='store_true', dest='password',
                        help='The password will be prompted after run the program. Defaults to env[LAUNCHER_PASSWORD].')
    parser.add_argument('--url', action='store', dest='url',
                        help='The authentication url of the form http://hostname:5000/v2.0 . Defaults to env[LAUNCHER_URL].')
    parser.add_argument('--tenant', action='store', dest='tenant',
                        help='The tenant name. Defaults to env[LAUNCHER_TENANT].')
    parser.add_argument('--instances', action='store', dest='instances', 
                        type=int, default=1, 
                        help='Number of instances to launch. Default: 1')

    subparsers = parser.add_subparsers(title='Subcommands', 
                                       description='Valid subcommands', 
                                       help='Subcommand availables for Images and Flavours.')

    image_parser = subparsers.add_parser('Image', help='Image options available')
    igexclusive = image_parser.add_mutually_exclusive_group()
    igexclusive.add_argument('--image', action='store', dest='image',
                             help="Image name to launch")
    igexclusive.add_argument('--ilist', action='store_true', dest='ilist',
                             help='List all images availables')

    flavour_parser = subparsers.add_parser('Flavour', help='Flavour options available')
    fgexclusive = flavour_parser.add_mutually_exclusive_group()
    fgexclusive.add_argument('--flavour', action='store', dest='flavour',
                             help='Flavour to use')
    fgexclusive.add_argument('--flist', action='store_true', dest='flist',
                             help='List all available flavours')

    security_group = parser.add_argument_group('Security groups options')
    sgexclusive = security_group.add_mutually_exclusive_group()
    sgexclusive.add_argument('--secgroup', help='Security group to use')
    sgexclusive.add_argument('--secgrouplist', help='List all available security groups')

    keypair_group = parser.add_argument_group('Keypair options')
    kgexclusive = keypair_group.add_mutually_exclusive_group()
    kgexclusive.add_argument('--keypair', help='Keypair to use')
    kgexclusive.add_argument('--keypairlist', help='List all available keypairs')

    return parser.parse_args()


def is_valid_url(nurl):
    url_ = UrlChecker(nurl)
    proto = url_.check_url_protocol()
    port = url_.check_url_port()
    if not proto or not port:
        return False
    return True

def get_credentials(param):
    try:
        return os.environ['LAUNCHER_' + param.upper()]
    except KeyError, e:
        print >> sys.stderr, 'Error. {0} not provided.'.format(e.message)
        sys.exit(3) 

def main():
    arguments = _parse_arguments()
    user = arguments.username if arguments.username else get_credentials('username')
    url = arguments.url if arguments.url else get_credentials('url')
    tenant = arguments.tenant if arguments.tenant else get_credentials('tenant')
    pwd = arguments.password
    if pwd:
        pwd = getpass.getpass().strip()
    else:
        pwd = get_credentials('password')
    if not is_valid_url(url):
        print >> sys.stderr, "Url not valid"
        return 2
    logininfo = Login(user, pwd, tenant, url)
    nova = do_openstack_login(logininfo)
    if arguments.image is None:
        get_image_name(nova)
    else:
        image = get_image_name(nova, arguments.image)
        print image
    """
    if flv is None:
        get_flavour_list(nova)
    else:
        flavour = get_flavour_list(nova, "m1.tiny")
    """
    return 0
    secgroup = get_security_group(nova)
    keypair = get_keypairs(nova)
    imgs = launch_virtual_machines(nova, "test", image, flavour, 
                                   secgroup=secgroup, kpair=keypair)
    return 0


if __name__ == '__main__':
    sys.exit(main())