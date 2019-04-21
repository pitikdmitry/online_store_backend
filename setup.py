#!/usr/bin/env python
# -*- coding: utf-8 -*

from setuptools import setup, find_packages


setup(
    name='weird-brains-backend',
    description='Backend API for weird-brains web-site',
    url='',
    python_requires='>=3.6',

    zip_safe=True,
    include_package_data=True,
    packages=find_packages(exclude=['tests']),
)
