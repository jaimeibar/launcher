# -*- coding: utf-8 -*-





import argparse
import sys
import getpass
import os
from launcher.login import Login
from launcher.urlchecker import UrlChecker
from launcher.makinator import do_openstack_login, get_image_name
from launcher.makinator import get_flavour_list, get_security_group, get_keypairs
from launcher.makinator import launch_virtual_machines




def _parse_arguments():
    parser = argparse.ArgumentParser(description="Launch virtual machines to OpenStack")

    parser.add_argument('-u', '--user', action='store', dest='username',
                        help='The username for login. Defaults to env[LAUNCHER_USERNAME].')
    parser.add_argument('-p', '--password', action='store_true', dest='password',
                        help='The password will be prompted after run the program. Defaults to env[LAUNCHER_PASSWORD].')
    parser.add_argument('--url', action='store', dest='url',
                        help='The authentication url of the form http://hostname:5000/v2.0 . Defaults to env[LAUNCHER_URL].')
    parser.add_argument('--tenant', action='store', dest='tenant',
                        help='The tenant name. Defaults to env[LAUNCHER_TENANT].')
    parser.add_argument('--instances', action='store', dest='instances',
                        type=int, default=1,
                        help='Number of instances to launch. Default: 1')
    parser.add_argument('--name', action='store', dest='name',
                        help='Name for the instances. Default: LAUNCHER_USERNAME')

    img_group = parser.add_argument_group('Image options')
    imagegroup = img_group.add_mutually_exclusive_group()
    imagegroup.add_argument('--image', action='store', dest='image',
                            help="Image name to launch")
    imagegroup.add_argument('--ilist', action='store_true', dest='ilist',
                            help='List all images availables')

    fl_group = parser.add_argument_group('Flavour options')
    flavourgroup = fl_group.add_mutually_exclusive_group()
    flavourgroup.add_argument('--flavour', action='store', dest='flavour',
                              help='Flavour to use')
    flavourgroup.add_argument('--flist', action='store_true', dest='flist',
                              help='List all available flavours')

    security_group = parser.add_argument_group('Security groups options')
    sgexclusive = security_group.add_mutually_exclusive_group()
    sgexclusive.add_argument('--secgroup', action='store', dest='secgroup',
                             help='Security group to use')
    sgexclusive.add_argument('--secgrouplist', action='store_true', dest='seclist',
                             help='List all available security groups')

    keypair_group = parser.add_argument_group('Keypair options')
    kgexclusive = keypair_group.add_mutually_exclusive_group()
    kgexclusive.add_argument('--keypair', action='store', dest='keypair',
                             help='Keypair to use')
    kgexclusive.add_argument('--keypairlist', action='store_true', dest='keylist',
                             help='List all available keypairs')

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
    nargs = len(sys.argv[1:])
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
    name = arguments.name
    image = arguments.image
    ilist = arguments.ilist
    flavour = arguments.flavour
    instances = arguments.instances
    flist = arguments.flist
    secgroup = arguments.secgroup
    seclist = arguments.seclist
    keypair = arguments.keypair
    keylist = arguments.keylist
    if any([ilist, flist, seclist, keylist]):
        if nargs > 1:
            print "Error. No extra parameters allowed"
            sys.exit(2)
        elif ilist:
            get_image_name(nova)
        elif flist:
            get_flavour_list(nova)
        elif seclist:
            get_security_group(nova)
        else:
            get_keypairs(nova)
    else:
        if all([image, flavour]):
            img = get_image_name(nova, image)
            flv = get_flavour_list(nova, flavour)
            name = user if name is None else name
            imgs = launch_virtual_machines(nova, name, img, flv,
                                           instances=instances,
                                           secgroup=secgroup, kpair=keypair)
        else:
            print >> sys.stderr, 'Not enough parameters'
            sys.exit(1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
