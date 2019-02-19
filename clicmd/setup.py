#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from setuptools import setup,find_packages

setup(
    name='dockercmd',
    version='0.1',
    py_modules=['dockercmd'],
    install_requires=[
        'Click',
    ],
    entry_points={
    'console_scripts':[
    'conn = dockercmd:connect',
    'fabric = dockercmd:fabric_init',
    'runcmd = dockercmd:fabric_run_cmd',
    ],
}
)