#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Sébastien Diemer <sebastien.diemer@mines-paristech.fr>

"""
Setup
"""
from setuptools import setup
from setuptools.command.install import install


URL = "http://dev.dataiku.com/~cstenac/dev-recruiting/us-census.db.gz"
LOCAL = "resources/us-census.db.gz"
LOCAL_EXTRACT = "resources/us-census.db"

class MyInstall(install):
    def run(self):
        install.run(self)
        import urllib
        urllib.urlretrieve(URL, LOCAL)
        from subprocess import call
        call(['gunzip', LOCAL])

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
    'name': 'webapp',
    'cmdclass': {'install': MyInstall}
}

setup(**config)
