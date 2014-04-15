# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


setup(name = 'launcher',
      version = '0.1',
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
      packages = find_packages(),
      include_package_data = True,
      zip_safe = False,
      install_requires = [line for line in open('requirements.txt')],
      entry_points = {
                      'console_scripts': [
                                          'launcher = launcher.cli:main'
                                          ]
                      }
      )
