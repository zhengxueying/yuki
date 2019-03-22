#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from setuptools import setup,find_packages

setup(
    name='scrum',
    version='0.1',
    py_modules=['scrum'],
    install_requires=[
        'Click',
    ],
    entry_points={
    'console_scripts':[
    'scrum = scrum:getAllTeamsInfoByNum',
    ],
}
)