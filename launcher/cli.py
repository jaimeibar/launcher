# -*- coding: utf-8 -*-


import argparse
import sys


def _parse_arguments():
    parser = argparse.ArgumentParser(description="Launch virtual machines to OpenStack")
    parser.add_argument('--user', '-u', action='store', required=True, 
                        dest='username', help='The username for login')
    parser.add_argument('--password', '-p', action='store', required=True,
                        dest='password', help='The password for that username')
    parser.add_argument('--url', action='store', required=True, dest='url',
                        help='The authentication url')
    parser.add_argument('--tenant', action='store', required=True, dest='tenant',
                        help="The tenant name")
    image = parser.add_argument_group('Image', 'Images')
    image.add_argument('--image', '-i', action='store', dest='image', 
                       help="Image name to launch")
    image.add_argument('--list', '-l', action='store', dest='list', 
                       help='Show all images availables')
    flavour = parser.add_argument_group('Flavour', 'Flavours')
    flavour.add_argument('--flavour', '-f', action='store', dest='flavour',
                         help='Show flavours availables')
    return parser.parse_args()


def main():
    arguments = _parse_arguments()
    print arguments


if __name__ == '__main__':
    sys.exit(main())