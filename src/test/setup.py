#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from setuptools import setup
setup(
    name='test',
    version='0.1',
    py_modules=['test'],
    install_requires=[
        'Click',
    ],
    entry_points={
    'console_scripts':[
    'testcli = test:cli',
    'justforfun=test:fun',
    ],
}
)