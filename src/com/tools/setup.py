#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from setuptools import setup,find_packages

setup(
    name='tools',
    version='0.1',
    py_modules=['cvtip'],
    install_requires=[
        'Click',
    ],
    entry_points={
    'console_scripts':[
    'cvtip = cvtip:convert_ip',
    ],
}
)