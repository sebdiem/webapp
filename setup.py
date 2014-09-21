#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Sébastien Diemer <sebastien.diemer@mines-paristech.fr>

"""
Setup
"""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A web application querying a database',
    'author': u'Sébastien Diemer',
    'url': 'https://github.com/sebdiem/webapp',
    'download_url': 'https://github.com/sebdiem/webapp',
    'author_email': 'diemersebastien@yahoo.fr',
    'version': '0.1',
    'install_requires': ['flask'],
    'packages': ['webapp'],
    'scripts': [],
    'name': 'webapp'
}

setup(**config)
