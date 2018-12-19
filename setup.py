#!/usr/bin/env python
"""
psycogreen -- setup script
"""

# Copyright (C) 2010-2018 Daniele Varrazzo <daniele.varrazzo@gmail.com>


from setuptools import setup

from psycogreen import __version__

classifiers = """
Development Status :: 5 - Production/Stable
License :: OSI Approved :: BSD License
Operating System :: OS Independent
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Topic :: Database
"""

kwargs = {}
try:
    kwargs['long_description'] = open('README.rst').read()
except Exception:
    pass

setup(
    name='psycogreen',
    description='psycopg2 integration with coroutine libraries',
    author='Daniele Varrazzo',
    author_email='daniele.varrazzo@gmail.com',
    url='https://bitbucket.org/dvarrazzo/psycogreen',
    license='BSD',
    packages=['psycogreen'],
    classifiers=[x for x in classifiers.split('\n') if x],
    version=__version__,
    **kwargs
)
