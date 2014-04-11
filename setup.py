# -*- coding: utf-8 -*-


from setuptools import setup, find_packages
from launcher import __version__


setup(name = 'launcher',
      version = __version__,
      description = 'Launch instances to OpenStack.',
      long_description = open('README.md').read(),
      classifiers = [
                     'Development Status :: 4 - Beta',
                     'Environment :: Console',
                     'Environment :: OpenStack',
                     'Intended Audience :: System Administrators',
                     'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
                     'Natural Language :: English',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python :: 2.7',
                     'Topic :: System',
                     'Topic :: Utilities'
                     ],
      keywords = '',
      author = 'Jaime Ibar',
      author_email = 'jim2k7@gmail.com',
      url = 'https://github.com/jim3k1/launcher',
      license = 'GPL2',
      packages = find_packages(exclude=['ez_setup']),
      include_package_data = True,
      zip_safe = False,
      install_requires = [line for line in open('requirements.txt')],
      entry_points = {
                      'console_scripts': [
                                          'launcher = launcher.cli:main'
                                          ]
                      }
      )
